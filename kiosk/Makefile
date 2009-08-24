OBJS = kiosk

CFLAGS = `pkg-config --cflags webkit-1.0`
LDFLAGS = `pkg-config --libs webkit-1.0`

CFLAGS += -Wall

all: $(OBJS)

clean:
	rm $(OBJS)
