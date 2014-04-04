all: libclient.so

submit: libclient.so
	@echo "$(shell cd ..;sh submit.sh c)"


libclient.so: ../library/*.cpp ../library/*.h
	$(MAKE) -C ../library/ libclient.so
	cp ../library/libclient.so libclient.so


libseastar.o: override CXXFLAGS += -fPIC
libseastar.o: seastar.cpp seastar.h
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c -o $@ $<


libseastar.so: seastar.o
	$(CXX) -shared -Wl,-soname,libseastar.so $(LDFLAGS) $(LOADLIBES) $(LDLIBS) $^ -o libseastar.so

clean:
	rm -f libclient.so
	rm -f *.pyc
	make -C ../library clean
