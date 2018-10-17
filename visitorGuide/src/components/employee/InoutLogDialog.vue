<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-btn slot="activator" flat small color="primary">확인</v-btn>
    <v-card>
      <v-card-title>
        <span class="headline">입실로그</span>
      </v-card-title>
      <v-data-table
        :headers="headers"
        class="elevation-1"
        :items="items"
      >
        <template slot="headerCell" slot-scope="props">
          <v-tooltip bottom>
            <span slot="activator">
              {{ props.header.text }}
            </span>
            <span>
              {{ props.header.text }}
            </span>
          </v-tooltip>
        </template>
        <template slot="items" slot-scope="props">
          <td class="text-xs-center">{{ props.item.time }}</td>
          <td class="text-xs-center">{{ props.item.state }}</td>
        </template>
      </v-data-table>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" flat @click="dialog = false">Cancel</v-btn>
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
        email: this.employee.email,
        headers: [
          { text: 'Time', align: 'center', sortable: false, value: 'time'},
          { text: 'State', align: 'center', value: 'state', sortable: false }
        ]
      }
    },
    computed: {
      items () {
        this.$store.dispatch('loadInouts', {id: this.email.split('@')[0]})
        return this.$store.getters.loadedInouts
      }
    },
    methods: {
    }
  }
</script>
