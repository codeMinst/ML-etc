<template>
  <v-container>
    <v-layout row justify-center>
      <v-flex xs12 sm6 offset-sm3>
        <h2>Create a new Employee</h2>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-flex xs12>
        <form @submit.prevent="onCreateEmployee">
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <img :src="imageUrl" height="150px" />
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <v-btn raised class="primary" @click="onPickFile"> Upload Image </v-btn>
              <input type="file" style="display: none;" ref="fileInput" accept="image/*" @change="onFilePicked" />
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <v-text-field name="name" label="Name" id="name" v-model="name" required></v-text-field>
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <v-text-field name="engName" label="English Name" id="engName" v-model="engName" required></v-text-field>
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <v-text-field name="email" label="email" id="email" v-model="email" required></v-text-field>
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <v-select
                :items="states"
                v-model="department"
                label="Department"
                autocomplete
              ></v-select>
              <!-- <v-text-field name="department" label="Department" id="department" v-model="department" required></v-text-field> -->
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <v-text-field name="position" label="Position" id="position" v-model="position" required></v-text-field>
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <v-text-field name="telNum" label="Number" id="telNum" v-model="telNum" required></v-text-field>
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <v-text-field name="tpNum" label="TP Number" id="tpNum" v-model="tpNum" required></v-text-field>
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <v-btn color="primary" dark @click.stop="trainingDialog = true">얼굴트레이닝</v-btn>
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
              <v-btn class="primary" :disabled="!formIsValid" type="submit">Create Meetup</v-btn>
            </v-flex>
          </v-layout>
        </form>
      </v-flex>
      <v-dialog v-model="trainingDialog" max-width="900px">
       <v-card row>
         <v-card-title>
           <span>얼굴인식트레이닝</span>
         </v-card-title>
         <v-card-text>
           <v-container grid-list-md>
             <v-layout wrap>
               <v-flex xs6 sm6 md6>
                 label : {{email}}
               </v-flex>
               <v-flex xs12 sm12 md12>
                 <v-btn color="primary" flat @click="labelCreate()">라벨등록</v-btn>
               </v-flex>
               <v-flex xs6 sm6 md6>
                 <video id="videoElement" ref="videoRef" src="" autoplay width="100%"></video>
               </v-flex>
               <v-flex xs12 sm12 md12>
                 <v-btn color="primary" flat @click="captureStart">등록시작</v-btn>
                 <v-btn color="primary" flat @click="captureEnd">등록종료</v-btn>
                <v-btn color="primary" flat @click="imageSend(email)">이미지전송</v-btn>
                <v-btn color="primary" flat @click="trainingStart(email)">트레이닝 시작</v-btn>
                <v-btn color="primary" flat @click="trainingTest">테스트</v-btn>
               </v-flex>
               <div id="thumbs"></div>
               <!--image-->
               <!-- <v-flex xs2>
                <v-card color="blue-grey darken-2" class="white--text">
                  1
                </v-card>
                <v-checkbox v-model="invites"></v-checkbox>
              </v-flex> -->
            </v-flex>
                <!--image-->
             </v-layout>
            </v-container>
          </v-card-text>
         <v-card-actions>
           <v-btn color="primary" flat @click.stop="trainingDialog=false">Close</v-btn>
         </v-card-actions>
       </v-card>
     </v-dialog>
    </v-layout>
  </v-container>
</template>

<script>
    export default {
        data() {
            return {
                name: this.name,
                imageUrl: '',
                department: '',
                engName: '',
                email: '',
                position: '',
                telNum: '',
                tpNum: '',
                image: null,
                a1: null,
                states: [
                    '기술서비스본부', '지원서비스본부', '전략사업본부', '경영지원본부', 'SI사업본부'
                ],
                trainingDialog: false,
                capture: null,
                formData: ''
            }
        },
        computed: {
            formIsValid() {
                return this.name !== '' && this.department !== '' && this.engName !== '' && this.telNum !== '' && this.tpNum !== '' && this.email !== ''
            }
        },
        methods: {
          onCreateEmployee() {
              if (!this.formIsValid) {
                  return
              }
              const employeeData = {
                  name: this.name,
                  image: this.image,
                  department: this.department,
                  engName: this.engName,
                  email: this.email,
                  telNum: this.telNum,
                  tpNum: this.tpNum,
                  position: this.position
              }
              this.$store.dispatch('createEmployee', employeeData)
              this.$router.push('/employees')
          },
          onPickFile() {
              this.$refs.fileInput.click()
          },
          onFilePicked(event) {
              const files = event.target.files
              let filename = files[0].name
              if (filename.lastIndexOf('.') <= 0) {
                  return alert('Please add a valid file!')
              }
              const fileReader = new FileReader()
              fileReader.addEventListener('load', () => {
                  this.imageUrl = fileReader.result
              })
              fileReader.readAsDataURL(files[0])
              this.image = files[0]
          },
          labelCreate() {
            this.$http.post('http://172.17.2.35:5000/api/register_faces', {
              name: this.email.split('@')[0]
            })
            .then((result) => {
              console.log(result)
              alert(result.data.msg)
              this.posts = result.data
            })
          },
          captureStart() {
            this.capture = setInterval(function(){
              var video = document.querySelector("#videoElement")
              var thumbs = document.getElementById("thumbs");
              var c = document.createElement("canvas");
              var ctx = c.getContext("2d");
              c.width = 320
              c.height = 240
              ctx.drawImage(video, 0, 0, 320, 240); thumbs.appendChild(c)},1000)
          },
          captureEnd() {
            clearInterval(this.capture)
          },
          imageSend() {
            var thumbs = document.getElementById("thumbs");
            var cells = thumbs.getElementsByTagName("canvas");
            var dataURLs=new Array()
            for (var i = 0; i < cells.length; i++) {
                var dataURL = cells[i].toDataURL("image/jpeg");
                dataURLs.push(dataURL)
            }
            this.$http.post('http://172.17.2.35:5000/api/register_image', {
              name:this.email.split('@')[0],
              dataURLs: dataURLs
            })
            .then((result) => {
              //alert(result.data.msg)
            })

          //  console.log("dataURI:"+dataURI)

          },
          trainingStart(email){
            alert(this.email.split('@')[0])
            this.$http.get('http://172.17.2.35:5000/api/request_training', {
              params: { // query string
                name: this.email.split('@')[0]
              }
            })
            .then((result) => {
              alert(result.data.msg)
            })
          },
          trainingTest(){

            var video = document.querySelector("#videoElement")
            var c = document.createElement("canvas");
            var ctx = c.getContext("2d");
            c.width = 320
            c.height = 240
            ctx.drawImage(video, 0, 0, 320, 240)
            var dataURL = c.toDataURL("image/jpeg");

            this.$http.post('http://172.17.2.35:5000/api/validate_face_recognition', {
              mode: "0",
              dataURL: dataURL
            })
            .then((result) => {
              console.log(result)
              alert(result.data.people[0].name+",  "+result.data.people[0].prob)
            })
          }
        },
        mounted: function() {

        },
        watch: {
            trainingDialog: function() {
                var video = document.querySelector("#videoElement")
                if (this.trainingDialog == true) {
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
                } else if (this.trainingDialog == false) {
                    video.pause();
                    video.src = ""
                    console.log("Vid off");
                }
            }
        }
    }
</script>
