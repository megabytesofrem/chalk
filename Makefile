CC = gcc
TARGET = libchalk
VERSION = 0.1.0
OS := $(shell uname)
ifeq ($(OS), Darwin)
	LIBS = -L/usr/local/opt/python3/Frameworks/Python.framework/Versions/Current/lib -lpython3.9
else
	LIBS = $(shell python3-config --libs)
endif

CFLAGS = $(shell python3-config --cflags)

ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif

all: $(TARGET).so $(TARGET).a

install: $(TARGET).so $(TARGET).a chalk.h
	install -d $(DESTDIR)$(PREFIX)/lib/
	install -m 644 $(TARGET).a $(DESTDIR)$(PREFIX)/lib/
	install -m 644 $(TARGET).so $(DESTDIR)$(PREFIX)/lib/
	install -d $(DESTDIR)$(PREFIX)/include/
	install -m 644 chalk.h $(DESTDIR)$(PREFIX)/include/

EXAMPLE-TARGET = chalk-example
EXAMPLE-OBJS = example.o chalk.o
example: $(EXAMPLE-OBJS)
	$(CC) $(EXAMPLE-OBJS) $(CFLAGS) $(LIBS) -o $(EXAMPLE-TARGET)
	./$(EXAMPLE-TARGET)

$(TARGET).a: chalk.o
	ar -rc $(TARGET).a chalk.o

$(TARGET).so: chalk.o
	$(CC) -shared $(CFLAGS) $(LIBS) chalk.o -o $(TARGET).so

.o: %.c
	$(CC) $(CFLAGS) -c $<

run: all
	./$(TARGET)

clean:
	rm *.o *.so *.a $(EXAMPLE-TARGET)
