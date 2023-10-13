(function ($) {
    'use strict';

    // Add JS code of Backend developer

	$('.input-file input[type=file]').on('change', function(){
		let file = this.files[0];
		$(this).closest('.input-file').find('.input-file-text').html(file.name);
	});

	// news_audio
	const playerSrc = document.getElementById('audio_source'),
		playBlock = document.querySelectorAll('.play-block'),
		playLink = document.querySelectorAll('.audio-source-item'),
		audioPlayer = document.querySelectorAll('.audio-player'),
		duration = document.querySelectorAll('.duration'),
		newsTitle = document.getElementById('news_title'),
		title = document.querySelectorAll('.news_title')

	duration.forEach((element, id)=>{
		const durationTime = audioPlayer[id].duration
		const time_min = Math.floor(durationTime / 60)
		const time_sec = (durationTime % 60).toFixed()
		const formattedTime = `${time_min < 10 ? '0' + time_min : time_min}:${time_sec < 10 ? '0' + time_sec : time_sec}`;
  		element.innerHTML = formattedTime
	})

	playerSrc.innerHTML = playLink[0].innerHTML
	newsTitle.innerHTML = title[0].innerHTML
	playBlock.forEach((block, id)=>{
		block.addEventListener('click', (e)=>{
			e.preventDefault()
			playerSrc.innerHTML = playLink[id].innerHTML
			newsTitle.innerHTML = title[id].innerHTML
		})
	})

	// news_video
	const videoSourse = document.getElementById('video_link'),
		videoLink = document.querySelectorAll('.video-link'),
		playVideo = document.querySelectorAll('.play-btn'),
		videoTitle = document.getElementById('video_title'),
		video = document.querySelectorAll('.video-title'),
		videoTime = document.querySelectorAll('.video_time'),
		videotime = document.querySelectorAll('.video-time')


		videotime.forEach((element, id) => {
			videoTime[id].addEventListener('loadedmetadata', () => {
				const duration = videoTime[id].duration;
				const time_min = Math.floor(duration / 60);
				const time_sec = Math.floor(duration % 60);
				const formattedTime = `${time_min < 10 ? '0' + time_min : time_min}:${time_sec < 10 ? '0' + time_sec : time_sec}`;
				element.innerHTML = formattedTime;
			});
		});

		playVideo.forEach((block, id)=>{
			block.addEventListener('click', (e)=>{
				e.preventDefault()
				videoSourse.innerHTML = videoLink[id].innerHTML
				videoTitle.innerHTML = video[id].innerHTML
			})
		})
})(jQuery);

