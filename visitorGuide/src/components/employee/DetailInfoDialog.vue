<template>
  <v-dialog width="350px" persistent v-model="detailDialog">
      <v-spacer></v-spacer>
      <v-btn icon slot="activator">
        <v-icon>favorite</v-icon>
      </v-btn>
    <v-card>
      <v-card-media :src="detailImageURl" height="300px">
        <v-layout column class="media">
          <v-spacer></v-spacer>
          <v-card-title class="white--text pl-5 pt-5">
            <div class="display-1 pl-5 pt-5">{{detailName}}</div>
          </v-card-title>
        </v-layout>
      </v-card-media>
      <v-list two-line>
        <v-list-tile @click="">
          <v-list-tile-action>
            <v-icon color="indigo">phone</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{detailTelNum}}</v-list-tile-title>
            <v-list-tile-sub-title>Number</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-icon>chat</v-icon>
          </v-list-tile-action>
        </v-list-tile>
        <v-list-tile @click="">
          <v-list-tile-action></v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{detailTpNum}}</v-list-tile-title>
            <v-list-tile-sub-title>TpNumber</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-icon>chat</v-icon>
          </v-list-tile-action>
        </v-list-tile>
        <v-divider inset></v-divider>
        <v-list-tile @click="">
          <v-list-tile-action>
            <v-icon color="indigo">mail</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>aliconnors@example.com</v-list-tile-title>
            <v-list-tile-sub-title>Personal</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile @click="">
          <v-list-tile-action></v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>ali_connors@example.com</v-list-tile-title>
            <v-list-tile-sub-title>Work</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-divider inset></v-divider>
      </v-list>
      <v-card-actions>
        <v-btn color="primary" flat @click.stop="detailDialog=false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    props: ['employee'],
    data () {
      return {
        detailDialog: false,
        detailName: '',
        detailTelNum: '',
        detailTpNum: '',
        detailImageURl: ''
      }
    },
    created () {
      if(this.employee.imageUrl == undefined){
        this.employee.imageUrl = 'https://cdn1.iconfinder.com/data/icons/profession-avatar-solid-2/48/53-512.png'
      }
      this.detailName= this.employee.name
      this.detailTelNum= this.employee.tel_num
      this.detailTpNum= this.employee.tp_num
      this.detailImageURl= this.employee.imageUrl
    }
  }
</script>
