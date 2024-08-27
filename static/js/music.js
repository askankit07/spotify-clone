// Adding play Pause functionalty   

const audioPlayer=document.querySelector("#audio-player")
const playPauseBtn=document.querySelector("#play-pause")
const play=document.querySelector("#play")
const pause=document.querySelector("#pause")

playPauseBtn.addEventListener('click', ()=>{
    if (audioPlayer.paused){
        audioPlayer.play();
        play.className="none"
        pause.classList.remove('none')
    }
    else{
        audioPlayer.pause();
        play.classList.remove('none')
        pause.className="none"
    }
})

// updating time and progress bar

const progress=document.querySelector('#progress')
const currentTimeElement=document.querySelector('#current-time')

audioPlayer.addEventListener('timeupdate', ()=>{
    const progressPercentage=(audioPlayer.currentTime / audioPlayer.duration) * 100
    progress.style.width=`${progressPercentage}%`

    // update current time text
    const currentMintes=Math.floor(audioPlayer.currentTime / 60)
    const currentSeconds=Math.floor(audioPlayer.currentTime - currentMintes * 60)
    currentTimeElement.textContent=`${currentMintes}:${currentSeconds.toString().padStart(2, '0')}`
})

// Updating progress bar according to the user

const progressBar=document.querySelector("#progress-bar")

progressBar.addEventListener('click',(e)=>{
    const progressBarWidth=progressBar.clientWidth
    const clickX=e.offsetX
    const duration=audioPlayer.duration

    audioPlayer.currentTime= (clickX / progressBarWidth) * duration
})

// Adding the Next and Prev functionlity

document.getElementById('next').addEventListener('click', ()=>{
    audioPlayer.currentTime= Math.min(audioPlayer.duration, audioPlayer.currentTime + 10)
})

document.getElementById('prev').addEventListener('click', ()=>{
    audioPlayer.currentTime= Math.min(audioPlayer.duration, audioPlayer.currentTime - 10)
})
