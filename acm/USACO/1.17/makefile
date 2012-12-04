SOURCE=beads.cpp

OBJ=$(addsuffix .o,$(basename $(SOURCE)))
TARGET=$(addsuffix .exe, $(basename $(SOURCE)))

$(TARGET):$(OBJ)
	g++ -o $(TARGET) $(OBJ)
	rm *.o
	
$(OBJ) : $(SOURCE)
	g++ -c $(SOURCE)
