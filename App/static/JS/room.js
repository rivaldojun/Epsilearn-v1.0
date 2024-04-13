const socket =io();
const myvideo = document.querySelector("#vd1");
const currentURL = window.location.href;
    // Diviser l'URL en segments en fonction du slash ("/")
    const segments = currentURL.split('/');
    // Récupérer le code après le deuxième slash
    const code = segments[4];
const roomid=code
let username;


const videoContainer = document.querySelector('#vcont');
const sub=document.getElementById("subtitles" )
const overlayContainer = document.querySelector('#overlay')
const continueButt = document.querySelector('.continue-name');
const nameField = document.querySelector('#name-field');
const videoButt = document.querySelector('.novideo');
const audioButt = document.querySelector('.audio');
const cutCall = document.querySelector('.cutcall');
const screenShareButt = document.querySelector('.screenshare');
const whiteboardButt = document.querySelector('.board-icon')
const whiteboardCont = document.querySelector('.whiteboard-cont');
whiteboardCont.style.visibility = 'hidden';
audioButt.style.backgroundColor = "red";
videoButt.style.backgroundColor = "red";
const canvas = document.querySelector("#whiteboard");
const annotation = document.querySelector(".annotations");
const toggle = document.querySelector(".toggle-btn");
annotation.style.visibility="hidden"
sub.style.display='none'
const ctx = canvas.getContext('2d');
const ctxs = [];
ctxs.push(ctx);
let currentcolor;
let pensize=3;
let tool="Stylo noir"
let currentCanvasIndex = 0;

function setColor(newcolor) {
    currentcolor=newcolor
    pensize=3
    tool="Stylo "+newcolor
    updateCurrentTool(tool,currentCanvasIndex);
}

function setEraser() {
    const eraserSizeInput = document.querySelector("#eraserSize");
    pensize = parseInt(eraserSizeInput.value, 10);
    currentcolor = 'white';
    tool="Gomme"
    updateCurrentTool(tool,currentCanvasIndex);
}

function resizeCanvas() {
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  drawCanvas();
}

function createNewPage() {
    const newCtx = canvas.cloneNode().getContext('2d');
    ctxs.push(newCtx);
    currentCanvasIndex = ctxs.length - 1;
    drawCanvas();
}

function drawCanvas() {
    const currentCtx = ctxs[currentCanvasIndex];
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(currentCtx.canvas, 0, 0);
}

function clearBoard() {
    if (window.confirm('Are you sure you want to clear the board? This cannot be undone.')) {
        const currentCtx = ctxs[currentCanvasIndex]; // Obtenez le contexte du canvas actuel
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Effacez le contenu du canvas actuel
    }
}

window.addEventListener('resize', resizeCanvas);

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

let isDrawing = false;
let lastX = 0;
let lastY = 0;
let boardVisisble=false;

function startDrawing(e) {
    isDrawing = true;
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

function draw(e) {
    if (!isDrawing) return;
    ctx.lineWidth = pensize;
    ctx.lineCap = 'round';
    ctx.strokeStyle = currentcolor;
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

function stopDrawing() {
    isDrawing = false;
    ctxs[currentCanvasIndex].drawImage(canvas, 0, 0);
}



// Ajoutez les événements tactiles pour les écrans tactiles
canvas.addEventListener('touchstart', startDrawingTouch);
canvas.addEventListener('touchmove', drawTouch);
canvas.addEventListener('touchend', stopDrawing);

let touchIdentifier = null;

function startDrawingTouch(e) {
    e.preventDefault();
    const touch = e.touches[0];
    touchIdentifier = touch.identifier;
    isDrawing = true;
    [lastX, lastY] = [touch.clientX - canvas.getBoundingClientRect().left, touch.clientY - canvas.getBoundingClientRect().top];
}

function drawTouch(e) {
    e.preventDefault();
    if (!isDrawing) return;
    const touch = Array.from(e.changedTouches).find(t => t.identifier === touchIdentifier);
    if (!touch) return;
    const offsetX = touch.clientX - canvas.getBoundingClientRect().left;
    const offsetY = touch.clientY - canvas.getBoundingClientRect().top;
    ctx.lineWidth = pensize;
    ctx.lineCap = 'round';
    ctx.strokeStyle = currentcolor;
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(offsetX, offsetY);
    ctx.stroke();
    [lastX, lastY] = [offsetX, offsetY];
}





const nextButton = document.getElementById("next");
const prevButton = document.getElementById("prev");

nextButton.addEventListener('click', () => {
    
    if (currentCanvasIndex < ctxs.length - 1) {
        currentCanvasIndex++;
        drawCanvas();
        updateCurrentTool(tool,currentCanvasIndex);
    } else {
        createNewPage();
        updateCurrentTool(tool,currentCanvasIndex);
    }
});

prevButton.addEventListener('click', () => {
    if (currentCanvasIndex > 0) {
        currentCanvasIndex--;
        updateCurrentTool(tool,currentCanvasIndex);
        drawCanvas();
        
    }
});

// Initial setup
resizeCanvas();
createNewPage();


function updateCurrentTool(toolName,pagenumber) {
    const currentToolElement = document.querySelector("#currentTool");
    const pageNumber = document.querySelector("#pageNumber");
    currentToolElement.textContent = `Tool: ${toolName}`;
    pageNumber.textContent = `Page  ${pagenumber}`;

}

// Appel pour mettre à jour l'outil au chargement de la page
updateCurrentTool(tool,currentCanvasIndex);

function saveCanvasAsImage(canvas, fileName) {
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const tempCtx = tempCanvas.getContext("2d");

    // Remplir le canvas temporaire avec un fond blanc
    tempCtx.fillStyle = "white";
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

    // Dessiner le contenu du canvas d'origine sur le canvas temporaire
    tempCtx.drawImage(canvas, 0, 0);

    // Convertir le canvas temporaire en une image PNG
    const link = document.createElement("a");
    link.href = tempCanvas.toDataURL("image/png");
    link.download = fileName;
    link.click();
}



function saveAllCanvasesAsZip() {
    

    const zip = new JSZip();

    ctxs.forEach((canvasContext, index) => {
        const canvasName = `canvas_${index + 1}.png`;

        // Créer un canvas temporaire avec fond blanc
        const tempCanvas = document.createElement("canvas");
        tempCanvas.width = canvasContext.canvas.width+600;
        tempCanvas.height = canvasContext.canvas.height+400;
        const tempCtx = tempCanvas.getContext("2d");
        tempCtx.fillStyle = "white";
        tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

        // Dessiner le contenu du canvas original sur le canvas temporaire
        tempCtx.drawImage(canvasContext.canvas, 0, 0);

        // Convertir le canvas temporaire en objet blob PNG
        const dataBlob = dataURLToBlob(tempCanvas.toDataURL("image/png"));

        // Ajouter le fichier au ZIP
        zip.file(canvasName, dataBlob);
    });

    zip.generateAsync({ type: "blob" }).then(content => {
        const link = document.createElement("a");
        link.href = URL.createObjectURL(content);
        link.download = "canvases.zip";
        link.click();
    });
    
}

// Fonction pour convertir le dataURL en objet blob
function dataURLToBlob(dataURL) {
    const arr = dataURL.split(",");
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
}


const downloadButton = document.getElementById("downloadButton");
cutCall.addEventListener("click", saveAllCanvasesAsZip);


//whiteboard js end


let videoAllowed = 0;
let audioAllowed = 0;

let micInfo = {};
let videoInfo = {};

let videoTrackReceived = {};

let mymuteicon = document.querySelector("#mymuteicon");
mymuteicon.style.visibility = 'visible';

let myvideooff = document.querySelector("#myvideooff");
myvideooff.style.visibility = 'visible';

const configuration = {
    iceServers: [
        {
            urls: 'turn:openrelay.metered.ca:80',
            username: 'openrelayproject',
            credential: 'openrelayproject'
        }
    ]
}

const mediaConstraints = { video: true, audio: true };

let connections = {};
let cName = {};
let audioTrackSent = {};
let videoTrackSent = {};

let mystream, myscreenshare;


// document.querySelector('.roomcode').innerHTML = `${roomid}`

 continueButt.addEventListener('click', () => {
            if (nameField.value == '') return;
            username = nameField.value;
            overlayContainer.style.visibility = 'hidden';
            document.querySelector("#myname").innerHTML = `${username} (You)`;
            
            // Émettre l'événement 'join room' avec les données du formulaire
            socket.emit("join room", { roomid: roomid, username: username });
        });
nameField.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        continueButt.click();
    }
});


        videoContainer.className = 'video-cont-single';

let peerConnection;

function handleGetUserMediaError(e) {
    switch (e.name) {
        case "NotFoundError":
            alert("Unable to open your call because no camera and/or microphone" +
                "were found.");
            break;
        case "SecurityError":
        case "PermissionDeniedError":
            break;
        default:
            alert("Error opening your camera and/or microphone: " + e.message);
            break;
    }

}


function reportError(e) {
    console.log(e);
    return;
}


function startCall() {

    navigator.mediaDevices.getUserMedia(mediaConstraints)
        .then(localStream => {
            myvideo.srcObject = localStream;
            myvideo.muted = true;
            localStream.getAudioTracks().forEach(track => {
                track.enabled = false;
            });

            localStream.getVideoTracks().forEach(track => {
                track.enabled = false;
            });

            localStream.getTracks().forEach(track => {
                for (let key in connections) {
                    connections[key].addTrack(track, localStream);
                    if (track.kind === 'audio')
                        audioTrackSent[key] = track;
                    else
                        videoTrackSent[key] = track;
                }
            })

        })
        .catch(handleGetUserMediaError);


}

function handleVideoOffer(offerData) {

    const { offer, sender_sid, sender_name, mic_status, video_status } = offerData;
    const sid = sender_sid;
    cName[sid] = sender_name;
    console.log('video offered received');
    micInfo[sid] = mic_status;
    videoInfo[sid] = video_status;
    connections[sid] = new RTCPeerConnection(configuration);
    connections[sid].onicecandidate = function (event) {
        if (event.candidate) {
            console.log('icecandidate fired');
            socket.emit('new icecandidate', { 'candidate': event.candidate, 'sid': sid });
        }
    };
    connections[sid].ontrack = function (event) {
        const existingVideo = document.getElementById(`video${sid}`);
    
        if (!existingVideo) {
        if (!document.getElementById(sid)) {
            console.log('track event fired');

            let vidCont = document.createElement('div');
            let newvideo = document.createElement('video');
            let name = document.createElement('div');
            let muteIcon = document.createElement('div');
            let videoOff = document.createElement('div');
            const bo = document.getElementById("grid-content");
            
            // Styliser le conteneur vidéo
            
            vidCont.classList.add('videos-box');
            vidCont.style.paddingTop='10px'
            
            muteIcon.classList.add('mutes-icon')
            videoOff.classList.add('videos-off')
            muteIcon.id = `mute${sid}`;
            videoOff.id = `vidoff${sid}`;
            muteIcon.innerHTML = `<i class="fas fa-microphone-slash"></i>`;
            videoOff.innerHTML = '<i class="fas fa-video-slash"></i>'
            muteIcon.style.position = 'absolute';
            muteIcon.style.bottom = '0';
            muteIcon.style.left = '90%';
            muteIcon.style.textAlign = 'center';
            muteIcon.style.color='red'
            videoOff.style.position = 'absolute';
            videoOff.style.bottom = '0';
            videoOff.style.left = '0';
            videoOff.style.textAlign = 'center';
            videoOff.style.color='red'


            
            // Styliser la vidéo
            newvideo.classList.add('videos-frame');
            newvideo.autoplay = true;
            newvideo.playsinline = true;
            newvideo.style.width = "200px";
            newvideo.style.height = "200px";
            newvideo.style.borderRadius='20px'
       
            newvideo.id = `video${sid}`;
            newvideo.srcObject = event.streams[0];
            
            // Styliser le nom de l'utilisateur
            name.classList.add('nametags');
            name.style.position = 'absolute';
            name.style.bottom = '0';
            name.style.left = '0';
            name.style.width = '100%';
            name.style.textAlign = 'center';
            name.style.fontWeight = 'bold';
            name.style.fontFamily = 'Kanit';
            name.style.backgroundColor = 'transparent';
            name.style.color = 'white';
            name.innerHTML = cName[sid];
            
            // Créer un conteneur pour le nom et l'ajouter au DOM
            let nameContainer = document.createElement('div');
            nameContainer.style.position = 'relative'; // Assurez-vous que le conteneur est positionné relativement
            nameContainer.appendChild(name);
            let muteContainer = document.createElement('div');
            muteContainer.style.position = 'relative'; // Assurez-vous que le conteneur est positionné relativement
            muteContainer.appendChild(muteIcon);
            let videoContainer = document.createElement('div');
            videoContainer.style.position = 'relative'; // Assurez-vous que le conteneur est positionné relativement
            videoContainer.appendChild(videoOff);
            
            
            // Ajouter les éléments au DOM
            vidCont.appendChild(newvideo);
            vidCont.appendChild(nameContainer);
            vidCont.appendChild(muteContainer);
            vidCont.appendChild(videoContainer);
            bo.appendChild(vidCont);
            

            if (micInfo[sid] == 'on')
                muteIcon.style.visibility = 'hidden';
            else
                muteIcon.style.visibility = 'visible';

            if (videoInfo[sid] == 'on')
                videoOff.style.visibility = 'hidden';
            else
                videoOff.style.visibility = 'visible';




        }
    }

    };

    connections[sid].onremovetrack = function (event) {
        if (document.getElementById(sid)) {
            document.getElementById(sid).remove();
            console.log('removed a track');
        }

    };

    connections[sid].onnegotiationneeded = function () {

        connections[sid].createOffer()
            .then(function (offer) {
                return connections[sid].setLocalDescription(offer);
            })
            .then(function () {

                socket.emit('video-offer', {
                    'offer': connections[sid].localDescription,
                    'sid': sid,
                    'cname': cName[sid],
                    'micinf': micInfo[sid],
                    'vidinf': videoInfo[sid]
                });

            })
            .catch(reportError);
    };

    let desc = new RTCSessionDescription(offer);

    connections[sid].setRemoteDescription(desc)
        .then(() => { return navigator.mediaDevices.getUserMedia(mediaConstraints) })
        .then((localStream) => {

            localStream.getTracks().forEach(track => {
                connections[sid].addTrack(track, localStream);
                console.log('added local stream to peer')
                if (track.kind === 'audio') {
                    audioTrackSent[sid] = track;
                    if (!audioAllowed)
                        audioTrackSent[sid].enabled = false;
                }
                else {
                    videoTrackSent[sid] = track;
                    if (!videoAllowed)
                        videoTrackSent[sid].enabled = false
                }
            })

        })
        .then(() => {
            return connections[sid].createAnswer();
        })
        .then(answer => {
            return connections[sid].setLocalDescription(answer);
        })
        .then(() => {
            // Lorsque vous voulez émettre la réponse vidéo
socket.emit('video-answer', { 'answer': connections[sid].localDescription, 'sid': sid });

        })
        .catch(handleGetUserMediaError);


}

function handleNewIceCandidate(candidate, sid) {
    console.log('new candidate received');
    var newcandidate = new RTCIceCandidate(candidate);

    connections[sid].addIceCandidate(newcandidate)
        .catch(reportError);
}

function handleVideoAnswer(answer, sid) {
    console.log('answered the offer')
    const ans = new RTCSessionDescription(answer);
    connections[sid].setRemoteDescription(ans);
}

//Thanks to (https://github.com/miroslavpejic85) for ScreenShare Code

screenShareButt.addEventListener('click', () => {
    screenShareToggle();
});
let screenshareEnabled = false;
function screenShareToggle() {
    let screenMediaPromise;
    if (!screenshareEnabled) {
        if (navigator.getDisplayMedia) {
            screenMediaPromise = navigator.getDisplayMedia({ video: true });
        } else if (navigator.mediaDevices.getDisplayMedia) {
            screenMediaPromise = navigator.mediaDevices.getDisplayMedia({ video: true });
        } else {
            screenMediaPromise = navigator.mediaDevices.getUserMedia({
                video: { mediaSource: "screen" },
            });
        }
    } else {
        screenMediaPromise = navigator.mediaDevices.getUserMedia({ video: true });
    }
    screenMediaPromise
        .then((myscreenshare) => {
            screenshareEnabled = !screenshareEnabled;
            for (let key in connections) {
                const sender = connections[key]
                    .getSenders()
                    .find((s) => (s.track ? s.track.kind === "video" : false));
                sender.replaceTrack(myscreenshare.getVideoTracks()[0]);
            }
            myscreenshare.getVideoTracks()[0].enabled = true;
            const newStream = new MediaStream([
                myscreenshare.getVideoTracks()[0], 
            ]);
            myvideo.srcObject = newStream;
            myvideo.muted = true;
            mystream = newStream;
            screenShareButt.innerHTML = (screenshareEnabled 
                ? `<i class="fas fa-desktop"></i><span class="tooltiptext">Stop Share Screen</span>`
                : `<i class="fas fa-desktop"></i><span class="tooltiptext">Share Screen</span>`
            );
            myscreenshare.getVideoTracks()[0].onended = function() {
                if (screenshareEnabled) screenShareToggle();
            };
        })
        .catch((e) => {
            alert("Unable to share screen:" + e.message);
            console.error(e);
        });
}

socket.on('video-offer', handleVideoOffer);

// socket.on('new icecandidate', handleNewIceCandidate);
socket.on('new icecandidate', function (data) {
    const candidate = data['candidate'];
    const senderSid = data['sender_sid'];
    handleNewIceCandidate(candidate, senderSid);
});

// Lorsque vous recevez la réponse vidéo
socket.on('video-answer', (data) => {
    const { answer, sender_sid } = data;
    console.log('answered the offer');
    const ans = new RTCSessionDescription(answer);
    connections[sender_sid].setRemoteDescription(ans);
});

socket.on('action', async (data) => {
    const msg=data['msg']
    const sid=data['sid']
    if (msg == 'mute') {
        console.log(sid + ' muted themself');
        document.querySelector(`#mute${sid}`).style.visibility = 'visible';
        micInfo[sid] = 'off';
    }
    else if (msg == 'unmute') {
        console.log(sid + ' unmuted themself');
        document.querySelector(`#mute${sid}`).style.visibility = 'hidden';
        micInfo[sid] = 'on';
    }
    else if (msg == 'videooff') {
        console.log(sid + 'turned video off');
        document.querySelector(`#vidoff${sid}`).style.visibility = 'visible';
        videoInfo[sid] = 'off';
    }
    else if (msg == 'videoon') {
        console.log(sid + 'turned video on');
        document.querySelector(`#vidoff${sid}`).style.visibility = 'hidden';
        videoInfo[sid] = 'on';
    }
})



socket.on('join room', async (data) => {
    const conc = data.peers;
    const cnames = data.socketname;
    const micinfo = data.micSocket;
    const videoinfo = data.videoSocket;
    socket.emit('getCanvas');
    if (cnames)
        cName = cnames;

    if (micinfo)
        micInfo = micinfo;

    if (videoinfo)
        videoInfo = videoinfo;


    console.log(cName);
    if (conc) {
        await conc.forEach(sid => {
            connections[sid] = new RTCPeerConnection(configuration);

            connections[sid].onicecandidate = function (event) {
                if (event.candidate) {
                    console.log('icecandidate fired');
                    socket.emit('new icecandidate', { 'candidate': event.candidate, 'sid': sid });
                }
            };

            connections[sid].ontrack = function (event) {
                const existingVideo = document.getElementById(`video${sid}`);
    
                if (!existingVideo) {
                if (!document.getElementById(sid)) {
                    console.log('track event fired');
                    let vidCont = document.createElement('div');
                    let newvideo = document.createElement('video');
                    let name = document.createElement('div');
                    let muteIcon = document.createElement('div');
                    let videoOff = document.createElement('div');
                    const bo = document.getElementById("grid-content");
                    
                    // Styliser le conteneur vidéo
                    vidCont.classList.add('videos-box');
                    vidCont.style.paddingTop='10px'
                    muteIcon.classList.add('mutes-icon')
                    videoOff.classList.add('videos-off')
                    muteIcon.id = `mute${sid}`;
                    videoOff.id = `vidoff${sid}`;
                    muteIcon.innerHTML = `<i class="fas fa-microphone-slash"></i>`;
                    videoOff.innerHTML = '<i class="fas fa-video-slash"></i>'
                    muteIcon.style.position = 'absolute';
                    muteIcon.style.bottom = '0';
                    muteIcon.style.left = '90%';
                    muteIcon.style.textAlign = 'center';
                    muteIcon.style.color='red'
                    videoOff.style.position = 'absolute';
                    videoOff.style.bottom = '0';
                    videoOff.style.left = '0';
                    videoOff.style.textAlign = 'center';
                    videoOff.style.color='red'


                    
                    // Styliser la vidéo
                    newvideo.classList.add('videos-frame');
                    newvideo.autoplay = true;
                    newvideo.playsinline = true;
                    newvideo.style.width = "200px";
                    newvideo.style.height = "200px";
                    newvideo.style.padding = '0';
                    newvideo.id = `video${sid}`;
                    newvideo.srcObject = event.streams[0];
                    
                    // Styliser le nom de l'utilisateur
                    name.classList.add('nametags');
                    name.style.position = 'absolute';
                    name.style.bottom = '0';
                    name.style.left = '0';
                    name.style.width = '100%';
                    name.style.textAlign = 'center';
                    name.style.fontWeight = 'bold';
                    name.style.fontFamily = 'Kanit';
                    name.style.backgroundColor = 'transparent';
                    name.style.color = 'white';
                    name.innerHTML = cName[sid];
                    
                    // Créer un conteneur pour le nom et l'ajouter au DOM
                    let nameContainer = document.createElement('div');
                    nameContainer.style.position = 'relative'; // Assurez-vous que le conteneur est positionné relativement
                    nameContainer.appendChild(name);
                    let muteContainer = document.createElement('div');
                    muteContainer.style.position = 'relative'; // Assurez-vous que le conteneur est positionné relativement
                    muteContainer.appendChild(muteIcon);
                    let videoContainer = document.createElement('div');
                    videoContainer.style.position = 'relative'; // Assurez-vous que le conteneur est positionné relativement
                    videoContainer.appendChild(videoOff);
                    
                    
                    // Ajouter les éléments au DOM
                    vidCont.appendChild(newvideo);
                    vidCont.appendChild(nameContainer);
                    vidCont.appendChild(muteContainer);
                    vidCont.appendChild(videoContainer);
                    bo.appendChild(vidCont);
                    
        
                    if (micInfo[sid] == 'on')
                        muteIcon.style.visibility = 'hidden';
                    else
                        muteIcon.style.visibility = 'visible';
        
                    if (videoInfo[sid] == 'on')
                        videoOff.style.visibility = 'hidden';
                    else
                        videoOff.style.visibility = 'visible';
        
    
        

                }
            }

            };

            connections[sid].onremovetrack = function (event) {
                if (document.getElementById(sid)) {
                    document.getElementById(sid).remove();
                }
            }

            connections[sid].onnegotiationneeded = function () {

                connections[sid].createOffer()
                    .then(function (offer) {
                        return connections[sid].setLocalDescription(offer);
                    })
                    .then(function () {

                        socket.emit('video-offer', {
                            'offer': connections[sid].localDescription,
                            'sid': sid,
                            'cname': cName[sid],
                            'micinf': micInfo[sid],
                            'vidinf': videoInfo[sid]
                        });

                    })
                    .catch(reportError);
            };

        });

        console.log('added all sockets to connections');
        startCall();

    }
    else {
        console.log('waiting for someone to join');
        navigator.mediaDevices.getUserMedia(mediaConstraints)
            .then(localStream => {
                myvideo.srcObject = localStream;
                myvideo.muted = true;
                mystream = localStream;
            })
            .catch(handleGetUserMediaError);
    }
})

socket.on('remove peer', sid => {
    if (document.getElementById(sid)) {
        document.getElementById(sid).remove();
    }

    delete connections[sid];
})


document.getElementById('')


videoButt.addEventListener('click', () => {

    if (videoAllowed) {
        for (let key in videoTrackSent) {
            videoTrackSent[key].enabled = false;
        }
        videoButt.innerHTML = `<i class="fas fa-video-slash"></i>`;
        videoAllowed = 0;
        videoButt.style.backgroundColor = "red";

        if (mystream) {
            mystream.getTracks().forEach(track => {
                if (track.kind === 'video') {
                    track.enabled = false;
                }
            })
        }

        myvideooff.style.visibility = 'visible';

        socket.emit('action', 'videooff');
    }
    else {
        for (let key in videoTrackSent) {
            videoTrackSent[key].enabled = true;
        }
        videoButt.innerHTML = `<i class="fas fa-video"></i>`;
        videoAllowed = 1;
        videoButt.style.backgroundColor = "blue";
        if (mystream) {
            mystream.getTracks().forEach(track => {
                if (track.kind === 'video')
                    track.enabled = true;
            })
        }


        myvideooff.style.visibility = 'hidden';

        socket.emit('action', 'videoon');
    }
})


var recognition = new webkitSpeechRecognition(); // Utilisez SpeechRecognition pour une implémentation standard

        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'fr-FR';

        recognition.onresult = function(event) {
            var result = event.results[event.resultIndex];
            if (result.isFinal) {
                var transcript = result[0].transcript;
                // Envoyez la transcription au serveur
                socket.emit('audio_transcription', { transcription: transcript });
            }
        };

        recognition.onerror = function(event) {
            console.error('Erreur de reconnaissance vocale:', event.error);
        };

        document.getElementById('startCapture').addEventListener('click', function() {
            const sub=document.getElementById("subtitles" )
            const cap=document.getElementById("startCapture")
            if(sub.style.display==='none'){
                sub.style.display='block'
                cap.style.backgroundColor='blue'
            }
            else{
                sub.style.display='none'
                cap.style.backgroundColor='#d8d8d8'
            }
            recognition.start();
        });

        socket.on('subtitles', function(data) {
            document.getElementById('subtitles').textContent = data.text;
        });

audioButt.addEventListener('click', () => {

    if (audioAllowed) {
        for (let key in audioTrackSent) {
            audioTrackSent[key].enabled = false;
        }
        audioButt.innerHTML = `<i class="fas fa-microphone-slash"></i>`;
        audioAllowed = 0;
        audioButt.style.backgroundColor = "red";
        if (mystream) {
            mystream.getTracks().forEach(track => {
                if (track.kind === 'audio')
                    track.enabled = false;
            })
        }

        mymuteicon.style.visibility = 'visible';

        socket.emit('action', 'mute');
    }
    else {
        for (let key in audioTrackSent) {
            audioTrackSent[key].enabled = true;
        }
        audioButt.innerHTML = `<i class="fas fa-microphone"></i>`;
        audioAllowed = 1;
        audioButt.style.backgroundColor = "blue";
        if (mystream) {
            mystream.getTracks().forEach(track => {
                if (track.kind === 'audio')
                    track.enabled = true;
            })
        }

        mymuteicon.style.visibility = 'hidden';

        socket.emit('action', 'unmute');
    }
})



whiteboardButt.addEventListener('click', () => {
    if (boardVisisble) {
        whiteboardCont.style.visibility = 'hidden';
        boardVisisble = false;
        annotation.style.visibility="hidden"
    }
    else {
        whiteboardCont.style.visibility = 'visible';
        boardVisisble = true;
        annotation.style.visibility="visible"
    }
})

cutCall.addEventListener('click', () => {
    const s=document.getElementById("overlays")
    s.style.display="block"
    // location.href = '/accueil';
})