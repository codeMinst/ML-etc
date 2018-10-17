<template>
  <v-card>
    <v-card-title>
      <v-spacer></v-spacer>
      <v-btn class="mx-0" to="/employee/new">
        Create
      </v-btn>
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
        <td class="text-xs-center">{{ props.item.name }}</td>
        <td class="text-xs-center">{{ props.item.eng_name }}</td>
        <td class="text-xs-center">{{ props.item.email }}</td>
        <td class="text-xs-center">{{ props.item.department }}</td>
        <td class="text-xs-center">{{ props.item.tel_num }}</td>
        <td class="text-xs-center">{{ props.item.tp_num }}</td>
        <td class="text-xs-center">
          <commute-log-dialog :employee="props.item"></commute-log-dialog>
        </td>
        <td class="text-xs-center">
          <inout-log-dialog :employee="props.item"></inout-log-dialog>
        </td>
        <td class="justify-center layout px-0">
          <edit-employee-dialog :employee="props.item"></edit-employee-dialog>
          <v-btn icon class="mx-0" @click="deleteItem(props.item.id)">
            <v-icon color="pink">delete</v-icon>
          </v-btn>
        </td>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
  export default {
    data () {
      return {
        headers: [
          { text: '이름', align: 'center', sortable: false, value: 'name'},
          { text: '영문이름', align: 'center', value: 'englishName', sortable: false },
          { text: '이메일', align: 'center', value: 'englishName', sortable: false },
          { text: '부서', align: 'center', value: 'department', sortable: false },
          { text: '전화번호', align: 'center', value: 'telNum', sortable: false },
          { text: 'TP번호', align: 'center', value: 'tpNum', sortable: false },
          { text: '출/퇴근', align: 'center', value: 'commute', sortable: false },
          { text: '입실', align: 'center', value: 'inosut', sortable: false },
          { text: 'Actions', value: 'name', sortable: false }
        ]
      }
  },
  computed: {
    items () {
      return this.$store.getters.loadedEmployees
    }
  },
  methods: {
    deleteItem (id) {
      this.$store.dispatch('deleteItems', {id: id})
    }
  }
}

</script>
