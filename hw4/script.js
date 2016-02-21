
//add new item to TO DO list from text field
function newListItem() {
	//get user-entered value from text field
	var addedItem = $('#newlistitem').val();
	//add to TO DO list
	$('#todolist').prepend("<li>" + addedItem +'</li><button onclick="moveToDone(this)">Done</button>');
	//reset text field to blank
	$('#newlistitem').val('');

}

//move item from ToDo list to done list
function moveToDone(focusButton) {
	//get list item corresponding to button
	var thisitem = $(focusButton).prev();
	//delete button and list item
	$(focusButton).remove();
	thisitem.remove();
	//put button and HTML from to do list item into done list
	$("#donelist").prepend('<button onclick="moveBackToDo(this)">Undo</button>');
	$("#donelist").prepend('<li>' + thisitem.html() + '</li>');

}
//placeholder for moving things back to todo list
function moveBackToDo (backButton){
	var undoneItem = $(backButton).prev();
	$(backButton).remove();
	undoneItem.remove();
	$("#todolist").prepend('<button onclick="moveToDone(this)">Done</button>');
	$("#todolist").prepend('<li>' + undoneItem.html() + '</li>');
}

