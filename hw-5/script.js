$(document).ready(function(){
	//set up page to clear placeholder text in search field on focus, and attach "callAPI" event to search button
	$('#userinput').focus(function() {
		$(this).val('');
		});

	$('#searchenter').click(function() {
		callAPI($('#userinput').val());
	});
});



// Event hander for calling the SoundCloud API using the user's search query
function callAPI(query) {
	// Remove any existing Stratus player with song from previous search
	$('#stratus').remove();

	$.get("https://api.soundcloud.com/tracks?client_id=b3179c0738764e846066975c2571aebb",
		{'q': query,
		'limit': '200'},
		function(data) {
			showResults(data);
			//console.log(data);
		},'json'
	);
}

function showResults (responseObject) {
//iterate over results, assign relevant values from response object to variables, and create divs to display them
	//remove previous search results and field value
	$('.result').remove();
	$('#userinput').val('');
	var resultsList = $('#resultslist');
	
	$.each(responseObject, function( i, value) {
		if (i<=19) {
		var index = i;
		
		//get song play URL
		var resultPlayURL = value.permalink_url;
		
		//get values from API call, create elements, and populate with values
		resultDiv = document.createElement('div');
		$(resultDiv).addClass('result');
		
		//replace artwork with placeholder image if null
		if (value.artwork_url != null) {
			resultArtURL = value.artwork_url;
		} else {
			resultArtURL = 'https://placeholdit.imgix.net/~text?txtsize=18&txt=100%C3%97100&w=100&h=100';
		}
		var resultImage = document.createElement('img');
		$(resultImage).addClass("resultimage");
		$(resultImage).attr("src", resultArtURL);
		
		var resultTitle = document.createElement('p');
		$(resultTitle).addClass('resulttitle');
		resultTitle.innerHTML = value.title;
		
		var resultArtist = document.createElement('p');
		$(resultArtist).addClass('resultartist');
		resultArtist.innerHTML = value.user.username;
		
		
		var playButton = document.createElement('button');
		$(playButton).addClass('playbutton');
		$(playButton).attr('type', 'button');
		$(playButton).attr('onclick', setPlayURL(resultPlayURL));
		playButton.innerHTML = 'Play';

		var listButton = document.createElement('button');
		$(listButton).addClass('listbutton');
		$(listButton).attr('type', 'button');
		$(listButton).attr('onclick', 'addToPlaylist(this)');
		listButton.innerHTML = 'Add';


		
		$(resultDiv).append(resultImage, resultTitle, resultArtist, playButton, listButton);
		resultsList.append(resultDiv);
		}
	});
}

//function to allow submission when "enter" is pressed, send song to Stratus?
//see https://stackoverflow.com/questions/4418819/submit-form-on-enter-when-in-text-field

//function to populate onclick attribute of song play button
function setPlayURL(trackURL) {
	return ('changeTrack(\'' + trackURL + '\')');
}


function addToPlaylist(addButton) {
	var playList = $('#playlist');
	//get div of selected song
	var songDiv = $(addButton).closest('div');
	
	//clone and add to playlist, change class for styling & selection
	var playDiv = $(songDiv).clone().prependTo(playList);
	$(playDiv).attr('class', 'playitem');
	
	//select "add" button and change to "remove"
	var removeButton = $(playDiv).find('.listbutton');
	$(removeButton).attr('onclick', 'removeFromPlaylist(this)');
	$(removeButton).attr('class', 'playitembutton');
	$(".playitembutton").text('Remove');

	//add buttons for playlist manipulation
	var upButton = document.createElement('button');
	$(upButton).text('Move Up');
	$(playDiv).append(upButton);
	$(upButton).attr('onclick', 'movePlaySong(this)');
	var downButton = document.createElement('button');
	$(downButton).text('Move Down');
	$(playDiv).append(downButton);
	$(downButton).attr('onclick', 'movePlaySong(this)');

}

function removeFromPlaylist(remButton) {
	var playDiv = $(remButton).closest('div');
	$(playDiv).remove();
}

function movePlaySong(moveButton) {
	//move song up or down in the playlist, depending on button clicked
	var typeOfMove = $(moveButton).text();
	var current = $(moveButton).closest('div');
	
	
	if (typeOfMove === 'Move Up') {
		$(current).insertBefore($(current).prev());
	} else {
		$(current).insertAfter($(current).next());
	}
}

// 'Play' button event handler - play the track in the Stratus player
function changeTrack(url) {
	// Remove any existing instances of the Stratus player
	$('#stratus').remove();

	// Create a new Stratus player using the clicked song's permalink URL
	$.stratus({
      key: "b3179c0738764e846066975c2571aebb",
      auto_play: true,
      align: "bottom",
      links: url
    });
}


