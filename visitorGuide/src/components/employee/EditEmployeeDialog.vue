<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-btn icon class="mx-0" slot="activator">
      <v-icon color="teal">edit</v-icon>
    </v-btn>
    <v-card>
      <v-card-title>
        <span class="headline">Edit Employee</span>
      </v-card-title>
      <v-card-text>
        <v-container grid-list-md>
          <v-layout row>
            <v-flex xs12>
              <form>
                <v-layout row>
                  <v-flex xs12 sm6 offset-sm3>
                    <v-text-field name="editName" label="Name" id="editName" v-model="editName" required></v-text-field>
                  </v-flex>
                </v-layout>
                <!-- <v-layout row>
                  <v-flex xs12 sm6 offset-sm3>
                    <v-btn raised class="primary" @click="onPickFile"> Upload Image </v-btn>
                    <input type="file" style="display: none;" ref="fileInput" accept="image/*" @change="onFilePicked" />
                  </v-flex>
                </v-layout> -->
                <v-layout row>
                  <v-flex xs12 sm6 offset-sm3>
                    <img :src="editImageUrl" height="150px" />
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs12 sm6 offset-sm3>
                    <v-text-field name="editDepartment" label="Department" id="editDepartment" v-model="editDepartment" required></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs12 sm6 offset-sm3>
                    <v-text-field name="editEngName" label="English Name" id="editEngName" v-model="editEngName" required></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs12 sm6 offset-sm3>
                    <v-text-field name="editPosition" label="Position" id="editPosition" v-model="editPosition" required></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs12 sm6 offset-sm3>
                    <v-text-field name="editTelNum" label="Number" id="editTelNum" v-model="editTelNum" required></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs12 sm6 offset-sm3>
                    <v-text-field name="editTpNum" label="TP Number" id="editTpNum" v-model="editTpNum" required></v-text-field>
                  </v-flex>
                </v-layout>
              </form>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" flat @click="dialog = false">Cancel</v-btn>
        <v-btn color="blue darken-1" flat @click="onSaveChanges" >Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    props: ['employee'],
    data () {
      return {
        dialog: false,
        editName: this.employee.name,
        editImageUrl: this.employee.imageUrl,
        editDepartment: this.employee.department,
        editEngName: this.employee.eng_name,
        editPosition: this.employee.position,
        editTelNum: this.employee.tel_num,
        editTpNum: this.employee.tp_num,
        editImage: null
      }
    },
    computed: {
      formIsValid () {
        return this.name !== '' && this.department !== '' && this.engName !== '' && this.telNum !== '' && this.tpNum
      }
    },
    methods: {
      onPickFile () {
        this.$refs.fileInput.click()
      },
      onFilePicked (event) {
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
      onSaveChanges () {
        this.dialog = false
        this.$store.dispatch('updateEmployeeData', {
          id: this.employee.id,
          name: this.name,
          department: this.department,
          engName: this.engName,
          telNum: this.telNum,
          tpNum: this.tpNum
        })
      }
    }
  }
</script>
