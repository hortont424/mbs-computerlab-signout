/*
 * Copyright (C) 2006, 2007 Apple Inc.
 * Copyright (C) 2007 Alp Toker <alp@atoker.com>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY APPLE COMPUTER, INC. ``AS IS'' AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL APPLE COMPUTER, INC. OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
 * OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <string.h>
#include <stdlib.h>
#include <gtk/gtk.h>
#include <webkit/webkit.h>
#include <libsoup/soup.h>

char signinURL[] = "http://127.0.0.1:8080/";

static GtkWidget * main_window = NULL;
static WebKitWebView * web_view = NULL;
static GSource * timer = NULL;
static GMount * backup_mount = NULL;
static GtkWidget * backup_button = NULL;

static gboolean backup_disk_inserted();
static void monitor_backup_disk();

static void close_cb(GtkWidget * widget, gpointer data);
static gboolean timer_reset_cb(gpointer data);
static void activity_cb(WebKitWebView * wv, GParamSpec * ps, gpointer data);
static void reload_cb(GtkWidget * widget, gpointer data);
static void shutdown_cb(GtkWidget * widget, gpointer data);
static void backup_cb(GtkWidget * widget, gpointer data);
static void backup_disk_changed_cb(GVolumeMonitor * volume_monitor,
                                   GMount * mount, gpointer user_data);

static void backup_disk_changed_cb(GVolumeMonitor * volume_monitor,
                                   GMount * mount, gpointer user_data)
{
    gtk_widget_set_sensitive(backup_button, backup_disk_inserted());
}

static void monitor_backup_disk()
{
    GVolumeMonitor * gvm = NULL;
    gvm = g_volume_monitor_get();
    g_signal_connect(G_OBJECT(gvm), "mount-added",
                     G_CALLBACK(backup_disk_changed_cb), NULL);
    g_signal_connect(G_OBJECT(gvm), "mount-removed",
                     G_CALLBACK(backup_disk_changed_cb), NULL);
}

static gboolean backup_disk_inserted()
{
    GVolumeMonitor * gvm = NULL;
    GList * mounts = NULL;
    
    gvm = g_volume_monitor_get();
    mounts = g_volume_monitor_get_mounts(gvm);
    
    if(!mounts)
        goto give_up;
    
    do
    {
        GFile * root = NULL;
        root = g_mount_get_root(mounts->data);
        
        if(strcmp(g_file_get_path(root), "/media/backups") == 0)
        {
            backup_mount = (GMount *)(mounts->data);
            return true;
        }
        
        g_object_unref(root);
    }
    while((mounts = g_list_next(mounts)) != NULL);

give_up:
    backup_mount = NULL;
    return false;
}

static void close_cb(GtkWidget * widget, gpointer data)
{
    gtk_main_quit();
}

static gboolean timer_reset_cb(gpointer data)
{
    reload_cb(NULL, NULL);
    
    return TRUE;
}

static void activity_cb(WebKitWebView * wv, GParamSpec * ps, gpointer data)
{
    // reset timer
    if(timer)
    {
        // destroy old timer
        g_source_destroy(timer);
    }
    
    // create new timer
    timer = g_timeout_source_new_seconds(10 * 60);
    g_source_set_callback(timer, timer_reset_cb, NULL, NULL);
    g_source_attach(timer, g_main_context_default());
}

static void shutdown_cb(GtkWidget * widget, gpointer data)
{
    GtkWidget * dialog = NULL;
    int res = 0;
    
    dialog = gtk_message_dialog_new(GTK_WINDOW(main_window),
                                    GTK_DIALOG_DESTROY_WITH_PARENT,
                                    GTK_MESSAGE_ERROR,
                                    GTK_BUTTONS_YES_NO,
                                    "Are you sure you want to shutdown?");
    res = gtk_dialog_run(GTK_DIALOG(dialog));
    gtk_widget_destroy(dialog);

    switch(res)
    {
        case GTK_RESPONSE_YES:
            system("sudo halt");
            gtk_main_quit();
            break;
        default:
            break;
    }
}

static void backup_cb(GtkWidget * widget, gpointer data)
{
    system("cd /home/mbs/src/mbs-computerlab-signout/; python ./backup.py");
    system("sudo umount /media/backups");
}

static void reload_cb(GtkWidget * widget, gpointer data)
{
    // Clear cookies
    SoupSession * session = NULL;
    SoupCookieJar * cj = NULL;
    GSList * cookies = NULL, * cookie_list = NULL;
    
    session = webkit_get_default_session();
    
    if(session == NULL)
        goto give_up;
    
    cj = (SoupCookieJar*)soup_session_get_feature(session,
                                                  soup_cookie_jar_get_type());
    
    if(cj == NULL)
        goto give_up;
    
    cookie_list = cookies = soup_cookie_jar_all_cookies(cj);
    
    if(cookies == NULL)
        goto give_up;
    
    do
    {
        soup_cookie_jar_delete_cookie(cj, ((SoupCookie*)(cookies->data)));
    }
    while((cookies = g_slist_next(cookies)) != NULL);

    g_slist_free(cookie_list);
    
    // Reload main page
give_up:
    webkit_web_view_load_uri(web_view, signinURL);
}

static GtkWidget * create_browser()
{
    GtkWidget * frame = gtk_frame_new(NULL);
    GtkWidget * scrolled_window = gtk_scrolled_window_new(NULL, NULL);
    gtk_scrolled_window_set_policy(GTK_SCROLLED_WINDOW(scrolled_window),
                                   GTK_POLICY_AUTOMATIC, GTK_POLICY_AUTOMATIC);

    web_view = WEBKIT_WEB_VIEW(webkit_web_view_new());
    g_signal_connect(web_view, "notify::load-status", G_CALLBACK(activity_cb),
                     NULL);

    gtk_container_add(GTK_CONTAINER(scrolled_window), GTK_WIDGET(web_view));
    gtk_container_add(GTK_CONTAINER(frame), GTK_WIDGET(scrolled_window));

    return frame;
}

static GtkWidget * create_toolbar()
{
    GtkWidget * toolbar = gtk_hbox_new(FALSE, 0);
    GtkWidget * item;

    item = gtk_button_new_with_label("Shutdown");
    g_signal_connect(G_OBJECT(item), "clicked", G_CALLBACK(shutdown_cb), NULL);
    gtk_box_pack_start(GTK_BOX(toolbar), item, FALSE, FALSE, 5);

    item = gtk_button_new_with_label("Backup");
    g_signal_connect(G_OBJECT(item), "clicked", G_CALLBACK(backup_cb), NULL);
    gtk_box_pack_start(GTK_BOX(toolbar), item, FALSE, FALSE, 5);
    gtk_widget_set_sensitive(item, backup_disk_inserted());
    backup_button = item;

    item = gtk_button_new_with_label("Reset");
    g_signal_connect(G_OBJECT(item), "clicked", G_CALLBACK(reload_cb), NULL);
    gtk_box_pack_end(GTK_BOX(toolbar), item, FALSE, FALSE, 5);

    return toolbar;
}

static GtkWidget * create_window()
{
    GtkWidget * window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    g_signal_connect(G_OBJECT(window), "hide", G_CALLBACK(close_cb), NULL);
    gtk_widget_set_name(window, "MBS Sign-in");

    return window;
}

int main(int argc, char ** argv)
{
    gtk_init(&argc, &argv);
    if(!g_thread_supported())
        g_thread_init(NULL);

    GtkWidget * vbox = gtk_vbox_new(FALSE, 0);
    gtk_box_pack_start(GTK_BOX(vbox), create_browser(), TRUE, TRUE, 0);
    gtk_box_pack_start(GTK_BOX(vbox), create_toolbar(), FALSE, FALSE, 5);

    main_window = create_window();
    gtk_container_add(GTK_CONTAINER(main_window), vbox);

    webkit_web_view_load_uri(web_view, signinURL);

    gtk_widget_grab_focus(GTK_WIDGET(web_view));
    gtk_widget_show_all(main_window);
    gtk_window_fullscreen(GTK_WINDOW(main_window));
    
    monitor_backup_disk();
    
    gtk_main();

    return 0;
}
