<template>
  <v-app>
    <v-layout column justify-center align-center>
      <v-container fluid grid-list-xl style="width:1000px;  overflow: hidden;">
        <v-layout wrap row style="width:100%; cursor: grab; cursor : -o-grab; cursor : -moz-grab; cursor : -webkit-grab;"
        class="dragscroll" >
            <v-flex v-for='card in employees1' :key='card.key'>
              <v-card :color='card.color' class='white--text' style="width:200px">
                <v-container fluid grid-list-lg>
                  <v-layout row>
                    <v-flex xs7>
                      <div>
                        <div class='headline' v-text='card.name'></div>
                        <div>{{card.department}},</div>
                        <div>{{card.position}}</div>
                      </div>
                    </v-flex>
                    <v-flex xs5>
                      <v-card-media
                        :src='card.imageUrl'
                        height='120px'
                        contain
                        @click.stop="workStartDialog = true"
                      >
                      </v-card-media>
                    </v-flex>
                  </v-layout>
                  <v-card-actions>
                    <detail-info-dialog v-if='userIsCreator' :employee="card"></detail-info-dialog>
                    <v-btn icon slot="activator" @click="doCall" @click.stop="callDialog = true">
                      <v-icon>call</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-container>
              </v-card>
            </v-flex>
        </v-layout>
        <v-layout wrap row>
            <v-flex v-for='card in employees2' :key='card.key'>
              <v-card :color='card.color' class='white--text' style="width:200px">
                <v-container fluid grid-list-lg>
                  <v-layout row>
                    <v-flex xs7>
                      <div>
                        <div class='headline' v-text='card.name'></div>
                        <div>{{card.department}},</div>
                        <div>{{card.position}}</div>
                      </div>
                    </v-flex>
                    <v-flex xs5>
                      <v-card-media
                        :src='card.imageUrl'
                        height='120px'
                        contain
                      >
                      </v-card-media>
                    </v-flex>
                  </v-layout>
                  <v-card-actions>
                    <detail-info-dialog v-if='userIsCreator' :employee="card"></detail-info-dialog>
                    <v-btn icon slot="activator" @click="doCall" @click.stop="callDialog = true">
                      <v-icon>call</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-container>
              </v-card>
            </v-flex>
        </v-layout>
        <v-layout wrap row>
            <v-flex v-for='card in employees3' :key='card.key'>
              <v-card :color='card.color'  class='white--text' style="width:200px">
                <v-container fluid grid-list-lg>
                  <v-layout row>
                    <v-flex xs7>
                      <div>
                        <div class='headline' v-text='card.name'></div>
                        <div>{{card.department}},</div>
                        <div>{{card.position}}</div>
                      </div>
                    </v-flex>
                    <v-flex xs5>
                      <v-card-media
                        :src='card.imageUrl'
                        height='120px'
                        contain
                      >
                      </v-card-media>
                    </v-flex>
                  </v-layout>
                  <v-card-actions>
                    <detail-info-dialog v-if='userIsCreator' :employee="card"></detail-info-dialog>
                    <v-btn icon slot="activator" @click="doCall" @click.stop="callDialog = true">
                      <v-icon>call</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-container>
              </v-card>
            </v-flex>
        </v-layout>
      </v-container>
    </v-layout>
    <v-dialog width="1000px" persistent v-model="callDialog">
        <v-spacer></v-spacer>
        <v-card>
         <v-card-title>
           <span class="headline">Call Connecting...</span>
         </v-card-title>
         <v-card-text>
           <v-container grid-list-md>
             <v-layout wrap>
              <div class="col-md-6 container" id="videos">
                  <div id="videoleft"></div>
                  <div id="videoright"></div>
              </div>
             </v-layout>
           </v-container>
         </v-card-text>
         <v-card-actions>
           <v-spacer></v-spacer>
           <v-btn color="blue darken-1" flat @click.stop="callDialog = false">Close</v-btn>
         </v-card-actions>
       </v-card>
    </v-dialog>
    <v-dialog v-model="workStartDialog" max-width="900px">
     <v-card row>
       <v-card-title>
         <span>출퇴근관리</span>
       </v-card-title>
       <v-card-text>
         <v-container grid-list-md>
           <v-layout wrap>
             <v-flex xs6 sm6 md6>
               <video id="video" src="" autoplay width="100%"></video>
             </v-flex>
             <v-flex xs12 sm12 md12>
               <v-btn color="primary" flat @click="workStart('0')">출근</v-btn>
             </v-flex>
             <v-flex xs12 sm12 md12>
               <v-btn color="primary" flat @click="workStart('1')">퇴근</v-btn>
             </v-flex>
          </v-flex>
              <!--image-->
           </v-layout>
          </v-container>
        </v-card-text>
       <v-card-actions>
         <v-btn color="primary" flat @click.stop="workStartDialog=false">Close</v-btn>
       </v-card-actions>
     </v-card>
   </v-dialog>
  </v-app>
</template>

<script>
  import {moment} from '../filters'
  export default {
    data () {
      return {
        callDialog  : false,
        server : null,
        //janus : null,
        //sipcall : null,
        opaqueId : "siptest-"+Janus.randomString(12),
        started : false,
        spinner : null,
        selectedApproach : null,
        registered : false,
        incoming : null,
        login: null,
        username: null,
        password: null,
        register: null,
        peer: null,
        call: null,
        dovideo: null,
        doulife: null,
        phone: null,
        workStartDialog: false,
        email: null
      }
    },
    filters: {
      moment
    },
    computed: {
      userIsCreator () {
        return 1 === 1
      },
      employees1 () {
        var new1 = this.$store.getters.loadedEmployees
        var new_={}
        var idx=0
        for(var k in new1) {
          if(k%3 == 0){
            new_[idx] = new1[k]
            if(new1[k].department == '기술서비스본부'){
              new_[idx].color='red'
            } else if(new1[k].department == '지원서비스본부'){
              new_[idx].color='orange'
            } else if(new1[k].department == '전략사업본부'){
              new_[idx].color='green'
            } else if(new1[k].department == '경영지원본부'){
              new_[idx].color='purple'
            } else if(new1[k].department == 'SI사업본부'){
              new_[idx].color='pink'
            } else {
              new_[idx].color='blue'
            }
            idx++
          }
        }
        return new_
      },
      employees2 () {
        var new1 = this.$store.getters.loadedEmployees
        var new_={}
        var idx=0
        for(var k in new1) {
          if(k%3 == 1){
            new_[idx] = new1[k]
            if(new1[k].department == '기술서비스본부'){
              new_[idx].color='red'
            } else if(new1[k].department == '지원서비스본부'){
              new_[idx].color='orange'
            } else if(new1[k].department == '전략사업본부'){
              new_[idx].color='green'
            } else if(new1[k].department == '경영지원본부'){
              new_[idx].color='purple'
            } else if(new1[k].department == 'SI사업본부'){
              new_[idx].color='pink'
            } else {
              new_[idx].color='blue'
            }
            idx++
          }
        }
        return new_
      },
      employees3 () {
        var new1 = this.$store.getters.loadedEmployees
        var new_={}
        var idx=0
        for(var k in new1) {
          if(k%3 == 2){
            new_[idx] = new1[k]
            if(new1[k].department == '기술서비스본부'){
              new_[idx].color='red'
            } else if(new1[k].department == '지원서비스본부'){
              new_[idx].color='orange'
            } else if(new1[k].department == '전략사업본부'){
              new_[idx].color='green'
            } else if(new1[k].department == '경영지원본부'){
              new_[idx].color='purple'
            } else if(new1[k].department == 'SI사업본부'){
              new_[idx].color='pink'
            } else {
              new_[idx].color='blue'
            }
            idx++
          }
        }
        return new_
      }
    },
    methods: {
      doCall () {
          var sipcall = this.$store.getters.sip
         // if(doUlife){
         //   username = "sip:" + username +"@o5vcs.masterbell.co.kr";
         // }else{
         //   username = "sip:" + username +"@masterbell.co.kr";
         // }
        var username = "sip:80000803@masterbell.co.kr";
         // Call this URI
         // doVideo = $('#dovideo').is(':checked');
         Janus.log("This is a SIP");
         //var sipcall = this.sipcall
         console.log(sipcall)
         sipcall.createOffer(
           {
             //trickle: false, //richinhim 2017.07.20
             media: {
               audioSend: true, audioRecv: true,		// We DO want audio
               videoSend: true, videoRecv: true	// We MAY want video
             },
             success: function(jsep) {
               Janus.debug("Got SDP!");
               Janus.debug(jsep);
               var body = { request: "call", uri: username };
               sipcall.send({"message": body, "jsep": jsep});
             },
             error: function(error) {
               Janus.log("WebRTC error..." + error);
               Janus.debug("WebRTC error..." + error);
               Janus.error("WebRTC error...", error);
              // bootbox.alert("WebRTC error... " + JSON.stringify(error));
             }
           });
         },
         workStart(state) {
           var video = document.querySelector("#video")
           var c = document.createElement("canvas");
           var ctx = c.getContext("2d");
           c.width = 320
           c.height = 240
           ctx.drawImage(video, 0, 0, 320, 240)
           var dataURL = c.toDataURL("image/jpeg");

           this.$http.post('http://172.17.2.35:5000/api/validate_face_recognition', {
             mode: state,
             dataURL: dataURL
           })
           .then((result) => {
             console.log(result)
             if(state == '0') {
               state = '출근'
             }else {
               state = '퇴근'
             }
             alert(result.data.people[0].name+",  "+result.data.people[0].prob)
             const attendData = {
               name: result.data.people[0].name,
               state: state,
               time: moment(new Date())
             }
             this.$store.dispatch('createWorkStartLog', attendData)
           })


         }
       },
       watch: {
           workStartDialog: function() {
               var video = document.querySelector("#video")
               if (this.workStartDialog == true) {
                   navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

                   if (navigator.getUserMedia) {
                       navigator.getUserMedia({
                           video: true
                       }, handleVideo, videoError);
                   }

                   function handleVideo(stream) {
                       video.src = window.URL.createObjectURL(stream);
                   }

                   function videoError() {
                       // do something
                   }
               } else if (this.workStartDialog == false) {
                   video.pause();
                   video.src = ""
                   console.log("Vid off");
               }
           }
       }
     }
</script>

<style>
  .container.grid-list-xl .layout .flex {
    padding: 12px;
    display: inline-block;
  }
  .layout.wrap {
    -ms-flex-wrap: initial;
    flex-wrap: initial;
  }

</style>
