import Vue from 'vue'
import Vuex from 'vuex'
import * as firebase from 'firebase'
import B from '../components/HelloWorld.vue';
import A from '../App.vue'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    employees: null,
    loadedEmployees: null,
    user: null,
    loadedAttends: null,
    sipcall: null,
    loadedInouts: null
  },
  components: {
      B
  },
  mutations: {
    setLoadedEmployees (state, payload) {
      state.loadedEmployees = payload
    },
    setLoadedAttends (state, payload) {
      state.loadedAttends = payload
    },
    setLoadedInouts (state, payload) {
      state.loadedInouts = payload
    },
    createEmployee (state, payload) {
      state.loadedEmployees.push(payload)
    },
    setUser (state, payload) {
      state.user = payload
    },
    setSipCall (state, payload) {
      state.sipcall = payload
    },

    setSensitivity (state, payload) {
      state.sensitivity = payload
    },
    setTemp1Canvas (state, payload) {
      state.temp1Canvas = payload
    },
    setTemp1Context (state, payload) {
      state.temp1Context = payload
    },
    setTemp2Canvas (state, payload) {
      state.temp2Canvas = payload
    },
    setTemp2Context (state, payload) {
      state.temp2Context = payload
    },
    setTopLeft (state, payload) {
      state.topLeft = payload
    },
    setBottomRight (state, payload) {
      state.bottomRight = payload
    },

    updateEmployee (state, payload) {
      const employee = state.loadedEmployees.find(employee => {
        return employee.id === payload.id
      })
      if (payload.name) {
        employee.name = payload.name
      }
      if (payload.department) {
        employee.department = payload.department
      }
      if (payload.engName) {
        employee.engName = payload.engName
      }
      if (payload.email) {
        employee.email = payload.email
      }
      if (payload.telNum) {
        employee.telNum = payload.telNum
      }
      if (payload.tpNum) {
        employee.tpNum = payload.tpNum
      }
    }
  },
  actions: {
    registerUserForMeetup ({commit, getters}, payload) {
    },
    loadEmployees ({commit}) {
      firebase.database().ref('employees').once('value')
      .then((data) => {
        const employees =[]
        const obj = data.val()
        for (let key in obj) {
          employees.push({
            id: key,
            name: obj[key].name,
            eng_name: obj[key].eng_name,
            position: obj[key].position,
            department: obj[key].department,
            tp_num: obj[key].tp_num,
            tel_num: obj[key].tel_num,
            imageUrl: obj[key].imageUrl,
            email: obj[key].email
          })
        }
        commit('setLoadedEmployees', employees)
      })
    },
    createEmployee ({commit, getters}, payload) {
      const employee = {
        name: payload.name,
        eng_name: payload.engName,
        email: payload.email,
        tp_num: payload.tpNum,
        tel_num: payload.telNum,
        position: payload.position,
        department: payload.department
      }
      let imageUrl
      let key
      firebase.database().ref('employees').push(employee)
      .then((data) => {
        key = data.key
        return key
      })
      .then(key => {
        const filename = payload.image.name
        const ext = filename.slice(filename.lastIndexOf('.'))
        return firebase.storage().ref('employees/' + key + '.' + ext).put(payload.image)
      })
      .then(fileData => {
        imageUrl = fileData.metadata.downloadURLs[0]
        return firebase.database().ref('employees').child(key).update({imageUrl: imageUrl})
      })
      .then(() => {
        commit('createEmployee', {
          ...employee,
          imageUrl: payload.imageUrl,
          id: key
        })
      })
      .catch((error) => {
        console.log(error)
      })
    },
    signUserIn ({commit}, payload) {
      firebase.auth().signInWithEmailAndPassword(payload.email, payload.password).then(
        user => {
          const newUser = {
            id: user.uid,
            registeredMeetups: [],
            fbkeys: {}
          }
          commit('setUser', newUser)
        }
      ).catch (
        error => {
          console.log(error)
        }
      )
    },
    autoSignIn ({commit}, payload) {
      commit('setUser', {
        id: payload.uid,
        registeredMeetups: [],
        fbkeys: {}
      })
    },
    fetchUserData ({commit, getters}) {
      firebase.database().ref('/users/' + getters.user.id + '/registrations/').once('value')
        .then(data => {
          const dataPairs = data.val()
          let registeredMeetups = []
          let swappedPairs = {}
          for (let key in dataPairs) {
            registeredMeetups.push(dataPairs[key])
            swappedPairs[dataPairs[key]] = key
          }
          const updatedUser = {
            id: getters.user.id,
            registeredMeetups: registeredMeetups,
            fbKeys: swappedPairs
          }
          commit('setUser', updatedUser)
        })
        .catch(error => {
          console.log(error)
        })
    },
    deleteItems ({commit}, payload) {
      firebase.database().ref('employees').child(payload.id).remove()
      .then(function() {
        console.log("Remove succeeded.")
        this.$store.dispatch('loadEmployees')
      })
      .catch(function(error) {
        console.log("Remove failed: " + error.message)
      })
    },
    updateEmployeeData ({commit}, payload) {
      const updateObj = {}
      if (payload.name) {
        updateObj.name = payload.name
      }
      if (payload.engName) {
        updateObj.engName = payload.engName
      }
      if (payload.telNum) {
        updateObj.telNum = payload.telNum
      }
      if (payload.department) {
        updateObj.department = payload.department
      }
      if (payload.tpNum) {
        updateObj.tpNum = payload.tpNum
      }
      if (payload.email) {
        updateObj.email = payload.email
      }
      firebase.database().ref('employees').child(payload.id).update(updateObj)
      .then(() => {
        commit('updateEmployee', payload)
      })
      .catch(error => {
        console.log(error)
      })
    },
    logout ({commit}) {
      firebase.auth().signOut()
      commit('setUser', null)
    },
    sipStart ({commit}) {
      var janus = null
      var opaqueId = "siptest-"+Janus.randomString(12)

      var started = false
      var spinner = null

      var selectedApproach = null
      var registered = false

      var incoming = null
      var sipcall = null;
      //this.detailTpNum= this.employee.tp_num
      Janus.init({debug: "all", callback: function() {
        $(this).attr('disabled', true).unbind('click');

        if(!Janus.isWebrtcSupported()) {
          alert("No WebRTC support... ")
          return
        }
        janus = new Janus({
          server : "https://testrtc.masterbell.co.kr:8089/janus",
          success: function(){
            janus.attach({
              plugin: "janus.plugin.sip",
              opaqueId: "siptest-"+Janus.randomString(12),
              success: function(pluginHandle) {
                sipcall = pluginHandle;
                console.log("this.sipcall"+sipcall)
                console.log("Plugin attached! (" + sipcall.getPlugin() + ", id=" + sipcall.getId() + ")")

                selectedApproach = 'secret'
                var sipserver = "sip:masterbell.co.kr"
                var register = {
                  "request" : "register",
                  "username" : "sip:12341234@masterbell.co.kr"
                }
                register["secret"] = "12341234"
                sipcall.send({"message": register});
                commit('setSipCall', sipcall)
              },
              error: function(error) {
                Janus.error("  -- Error attaching plugin...", error);
                alert("  -- Error attaching plugin... " + error);
              },
              consentDialog: function(on) {
									Janus.debug("Consent dialog should be " + (on ? "on" : "off") + " now");
									if(on) {
										// Darken screen and show hint
										$.blockUI({
											message: '<div><img src="up_arrow.png"/></div>',
											css: {
												border: 'none',
												padding: '15px',
												backgroundColor: 'transparent',
												color: '#aaa',
												top: '10px',
												left: (navigator.mozGetUserMedia ? '-100px' : '300px')
											} });
									} else {
										// Restore screen
										$.unblockUI();
									}
								},
								mediaState: function(medium, on) {
									Janus.log("Janus " + (on ? "started" : "stopped") + " receiving our " + medium);
								},
								webrtcState: function(on) {
									Janus.log("Janus says our WebRTC PeerConnection is " + (on ? "up" : "down") + " now");
									$("#videoleft").parent().unblock();
								},
								onmessage: function(msg, jsep) {

                  function handleVideo(stream) {
                      video.src = window.URL.createObjectURL(stream);
                  }


									Janus.debug(" ::: Got a message :::");
									Janus.debug(msg);
									// Any error?
									var error = msg["error"];
									if(error != null && error != undefined) {
										if(!registered) {
											$('#server').removeAttr('disabled');
											$('#username').removeAttr('disabled');
											$('#authuser').removeAttr('disabled');
											$('#displayname').removeAttr('disabled');
											$('#password').removeAttr('disabled');
											$('#register').removeAttr('disabled').click(registerUsername);
											$('#registerset').removeAttr('disabled');
										} else {
											// Reset status
											sipcall.hangup();
											$('#dovideo').removeAttr('disabled').val('');
											$('#peer').removeAttr('disabled').val('');
											// $('#call').removeAttr('disabled').html('Call')
											// 	.removeClass("btn-danger").addClass("btn-success")
											// 	.unbind('click').click(doCall);
										}
										alert(error);
										return;
									}
									var result = msg["result"];
									if(result !== null && result !== undefined && result["event"] !== undefined && result["event"] !== null) {
										var event = result["event"];
										if(event === 'registration_failed') {
											Janus.warn("Registration failed: " + result["code"] + " " + result["reason"]);
											$('#server').removeAttr('disabled');
											$('#username').removeAttr('disabled');
											$('#authuser').removeAttr('disabled');
											$('#displayname').removeAttr('disabled');
											$('#password').removeAttr('disabled');
											$('#register').removeAttr('disabled').click(registerUsername);
											$('#registerset').removeAttr('disabled');
											alert(result["code"] + " " + result["reason"]);
											return;
										}
										if(event === 'registered') {
											Janus.log("Successfully registered as " + result["username"] + "!");
											$('#you').removeClass('hide').show().text("Registered as '" + result["username"] + "'");
											// TODO Enable buttons to call now
											if(!registered) {
												registered = true;
												// $('#phone').removeClass('hide').show();
												// $('#call').unbind('click').click(doCall);
												// $('#peer').focus();
											}
										} else if(event === 'calling') {
											Janus.log("Waiting for the peer to answer...");
											// TODO Any ringtone?
											$('#call').removeAttr('disabled').html('Hangup')
												  .removeClass("btn-success").addClass("btn-danger")
												  .unbind('click').click('doHangup');
										} else if(event === 'incomingcall') {
											Janus.log("Incoming call from " + result["username"] + "!");
											var doAudio = true, doVideo = true;
											var offerlessInvite = false;
											if(jsep !== null && jsep !== undefined) {
												// What has been negotiated?
												doAudio = (jsep.sdp.indexOf("m=audio ") > -1);
												doVideo = (jsep.sdp.indexOf("m=video ") > -1);
												Janus.debug("Audio " + (doAudio ? "has" : "has NOT") + " been negotiated");
												Janus.debug("Video " + (doVideo ? "has" : "has NOT") + " been negotiated");
											} else {
												Janus.log("This call doesn't contain an offer... we'll need to provide one ourselves");
												offerlessInvite = true;
												// In case you want to offer video when reacting to an offerless call, set this to true
												doVideo = false;
											}
											// Any security offered? A missing "srtp" attribute means plain RTP
											var rtpType = "";
											var srtp = result["srtp"];
											if(srtp === "sdes_optional")
												rtpType = " (SDES-SRTP offered)";
											else if(srtp === "sdes_mandatory")
												rtpType = " (SDES-SRTP mandatory)";
											// Notify user
											bootbox.hideAll();
											var extra = "";
											if(offerlessInvite)
												extra = " (no SDP offer provided)"
											incoming = bootbox.dialog({
												message: "Incoming call from " + result["username"] + "!" + rtpType + extra,
												title: "Incoming call",
												closeButton: false,
												buttons: {
													success: {
														label: "Answer",
														className: "btn-success",
														callback: function() {
															incoming = null;
															$('#peer').val(result["username"]).attr('disabled', true);
															// Notice that we can only answer if we got an offer: if this was
															// an offerless call, we'll need to create an offer ourselves
															var sipcallAction = (offerlessInvite ? sipcall.createOffer : sipcall.createAnswer);
															sipcallAction(
																{
																	jsep: jsep,
																	media: { audio: doAudio, video: doVideo },
																	success: function(jsep) {
																		Janus.debug("Got SDP " + jsep.type + "! audio=" + doAudio + ", video=" + doVideo);
																		Janus.debug(jsep);
																		var body = { request: "accept" };
																		// Note: as with "call", you can add a "srtp" attribute to
																		// negotiate/mandate SDES support for this incoming call.
																		// The default behaviour is to automatically use it if
																		// the caller negotiated it, but you may choose to require
																		// SDES support by setting "srtp" to "sdes_mandatory", e.g.:
																		//		var body = { request: "accept", srtp: "sdes_mandatory" };
																		// This way you'll tell the plugin to accept the call, but ONLY
																		// if SDES is available, and you don't want plain RTP. If it
																		// is not available, you'll get an error (452) back. You can
																		// also specify the SRTP profile to negotiate by setting the
																		// "srtp_profile" property accordingly (the default if not
																		// set in the request is "AES_CM_128_HMAC_SHA1_80")
																		sipcall.send({"message": body, "jsep": jsep});
																		$('#call').removeAttr('disabled').html('Hangup')
																			.removeClass("btn-success").addClass("btn-danger")
																			.unbind('click').click('doHangup');
																	},
																	error: function(error) {
																		Janus.error("WebRTC error:", error);
																		alert("WebRTC error... " + JSON.stringify(error));
																		// Don't keep the caller waiting any longer, but use a 480 instead of the default 486 to clarify the cause
																		var body = { "request": "decline", "code": 480 };
																		sipcall.send({"message": body});
																	}
																});
														}
													},
													danger: {
														label: "Decline",
														className: "btn-danger",
														callback: function() {
															incoming = null;
															var body = { "request": "decline" };
															sipcall.send({"message": body});
														}
													}
												}
											});
										} else if(event === 'accepting') {
											// Response to an offerless INVITE, let's wait for an 'accepted'
										} else if(event === 'progress') {
											Janus.log("There's early media from " + result["username"] + ", wairing for the call!");
											Janus.log(jsep);
											// Call can start already: handle the remote answer
											if(jsep !== null && jsep !== undefined) {
												sipcall.handleRemoteJsep({jsep: jsep, error: function(){alert('error')}  });
											}
											toastr.info("Early media...");
										} else if(event === 'accepted') {
											Janus.log(result["username"] + " accepted the call!");
											Janus.log(jsep);
											// Call can start, now: handle the remote answer
											if(jsep !== null && jsep !== undefined) {
												sipcall.handleRemoteJsep({jsep: jsep, error: function(){alert('error')}});
											}
											toastr.success("Call accepted!");
										} else if(event === 'hangup') {
                      B.data().callDialog = false
											if(incoming != null) {
												incoming.modal('hide');
												incoming = null;
											}
											Janus.log("Call hung up (" + result["code"] + " " + result["reason"] + ")!");
											alert(result["code"] + " " + result["reason"]);
											// Reset status
											sipcall.hangup();
											$('#dovideo').removeAttr('disabled').val('');
											$('#peer').removeAttr('disabled').val('');
											// $('#call').removeAttr('disabled').html('Call')
											// 	.removeClass("btn-danger").addClass("btn-success")
											// 	.unbind('click').click(doCall);
										}
									}
								},
								onlocalstream: function(stream) {
									console.log(" ::: Got a local stream :::");
									console.log(stream);
									$('#videos').removeClass('hide').show();
									if($('#myvideo').length === 0)
										$('#videoleft').append('<video class="rounded centered" width=320 height=240 id="myvideo" autoplay muted="muted" playsinline/>');
									Janus.attachMediaStream($('#myvideo').get(0), stream);
									$("#myvideo").get(0).muted = "muted";
									if(sipcall.webrtcStuff.pc.iceConnectionState !== "completed" &&
											sipcall.webrtcStuff.pc.iceConnectionState !== "connected") {
										// $("#videoleft").parent().block({
										// 	message: '<b>Calling...</b>',
										// 	css: {
										// 		border: 'none',
										// 		backgroundColor: 'transparent',
										// 		color: 'white'
										// 	}
										// });
										// No remote video yet
										$('#videoright').append('<video class="rounded centered" id="waitingvideo" width=320 height=240 playsinline/>');
										if(spinner == null) {
											var target = document.getElementById('videoright');
											spinner = new Spinner({top:100}).spin(target);
										} else {
											spinner.spin();
										}
									}
									var videoTracks = stream.getVideoTracks()
									if(videoTracks === null || videoTracks === undefined || videoTracks.length === 0) {
										// No webcam
										$('#myvideo').hide();
										if($('#videoleft .no-video-container').length === 0) {
											$('#videoleft').append(
												'<div class="no-video-container">' +
													'<i class="fa fa-video-camera fa-5 no-video-icon"></i>' +
													'<span class="no-video-text">No webcam available</span>' +
												'</div>');
										}
									} else {
										$('#videoleft .no-video-container').remove();
										$('#myvideo').removeClass('hide').show();
									}
								},
                onremotestream: function(stream) {
									Janus.debug(" ::: Got a remote stream :::");
									Janus.debug(stream);
									if($('#remotevideo').length === 0) {
										//$('#videoright').parent().find('h3').html('Send DTMF: <span id="dtmf" class="btn-group btn-group-xs"></span>');
										$('#videoright').append('<video class="rounded centered hide" id="remotevideo" width=320 height=240 autoplay playsinline/>');

										// Show the peer and hide the spinner when we get a playing event
										$("#remotevideo").bind("playing", function () {
											$('#waitingvideo').remove();
											if(this.videoWidth)
												$('#remotevideo').removeClass('hide').show();
											if(spinner !== null && spinner !== undefined)
												spinner.stop();
											spinner = null;
										});
									}
									Janus.attachMediaStream($('#remotevideo').get(0), stream);
									var videoTracks = stream.getVideoTracks();
									if(videoTracks === null || videoTracks === undefined || videoTracks.length === 0) {
										// No remote video
										$('#remotevideo').hide();
										if($('#videoright .no-video-container').length === 0) {
											$('#videoright').append(
												'<div class="no-video-container">' +
													'<i class="fa fa-video-camera fa-5 no-video-icon"></i>' +
													'<span class="no-video-text">No remote video available</span>' +
												'</div>');
										}
									} else {
										$('#videoright .no-video-container').remove();
										$('#remotevideo').removeClass('hide').show();
									}
								},
								oncleanup: function() {
									Janus.log(" ::: Got a cleanup notification :::");
                  B.data().callDialog = false
									$('#myvideo').remove();
									$('#waitingvideo').remove();
									$('#remotevideo').remove();
									$('.no-video-container').remove();
									$('#videos').hide();

								}
            })
          },
          error: function(error) {
            Janus.error(error);
            alert(error, function() {
              window.location.reload();
            });
          },
          destroyed: function() {
            window.location.reload();
          }
        })
      }})
    },
    createWorkStartLog ({commit, getters}, payload) {
      const attend = {
        name: payload.name,
        time: payload.time,
        state: payload.state
      }
      let key
      firebase.database().ref('attend').push(attend)
      .then((data) => {
        key = data.key
      })
      .catch((error) => {
        console.log(error)
      })
    },
    loadAttends ({commit}, payload){
      firebase.database().ref('attend').once('value')
      .then((data) => {
        const attends =[]
        const obj = data.val()
        for (let key in obj) {
          attends.push({
             time: obj[key].time,
             state: obj[key].state
          })
        }
        commit('setLoadedAttends', attends)
      })
    },
    loadInouts ({commit}, payload){
      firebase.database().ref('inout').once('value')
      .then((data) => {
        const inouts =[]
        const obj_ = data.val()
        for (let key in obj_) {
          inouts.push({
             time: obj_[key].time,
             state: obj_[key].state
          })
        }
        commit('setLoadedInouts', inouts)
      })
    }
  },
  getters: {
    loadedEmployees (state) {
      return state.loadedEmployees
    },
    user (state) {
      return state.user
    },
    sip (state) {
      return state.sipcall
    },
    loadedAttends (state) {
      return state.loadedAttends
    },
    loadedInouts (state) {
      return state.loadedInouts
    }
  }
})
