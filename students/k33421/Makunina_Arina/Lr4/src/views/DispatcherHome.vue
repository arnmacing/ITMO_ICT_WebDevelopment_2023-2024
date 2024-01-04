<template>
  <v-container class="mt-10">
    <v-row justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title>Расписание</v-card-title>
          <v-card-actions>
            <v-btn text color="primary" @click="openSelectionDialog">Выбрать группу и семестр</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="schedule.length > 0">
      <v-col v-for="item in schedule" :key="item.id" cols="12" sm="6" md="4">
        <v-card>
          <v-card-title>{{ item.discipline.name }}</v-card-title>
          <v-card-subtitle>{{ item.time_slot.day_of_week_display }} {{ item.time_slot.start_time }} - {{ item.time_slot.end_time }}</v-card-subtitle>
          <v-card-text>
            <div>Преподаватель: {{ item.teacher.name }}</div>
            <div>Аудитория: {{ item.room.name }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>


    <!-- Add separate dialogs for group and semester selection -->
    <v-dialog v-model="groupDialog" persistent max-width="400px">
      <v-card>
        <v-card-title>Выберите группу</v-card-title>
        <v-card-text>
          <v-checkbox v-model="selectedGroups[group]" :label="group" v-for="group in groups" :key="group" />
        </v-card-text>
        <v-card-actions>
          <v-btn @click="closeGroupDialog">Отмена</v-btn>
          <v-btn @click="openSemesterDialog">Далее</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="semesterDialog" persistent max-width="400px">
      <v-card>
        <v-card-title>Выберите семестр</v-card-title>
        <v-card-text>
          <v-checkbox v-model="selectedSemesters[semester]" :label="semester" v-for="semester in semesters" :key="semester" />
        </v-card-text>
        <v-card-actions>
          <v-btn @click="closeSemesterDialog">Отмена</v-btn>
          <v-btn @click="goToSchedule">Перейти</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref } from 'vue'
const schedule = ref([])

const router = useRouter()

const groupDialog = ref(false)
const semesterDialog = ref(false)
const groups = ['К3423', 'К3342', 'К3240', 'К3142']
const semesters = ['1', '2']
const selectedGroups = ref({})
const selectedSemesters = ref({})

const openSelectionDialog = () => {
  groupDialog.value = true
}

const closeGroupDialog = () => {
  groupDialog.value = false
}

const openSemesterDialog = () => {
  groupDialog.value = false
  semesterDialog.value = true
}

const closeSemesterDialog = () => {
  semesterDialog.value = false
}

const goToSchedule = async () => {
  const selectedGroup = Object.entries(selectedGroups.value).find(([group, value]) => value)?.[0];
  const selectedSemester = Object.entries(selectedSemesters.value).find(([semester, value]) => value)?.[0];

  if (selectedGroup && selectedSemester) {
    console.log("Fetching schedule...");
    try {
      await fetchSchedule(selectedGroup, selectedSemester); // fetchSchedule should set the schedule.value
      console.log("Schedule fetched:", schedule.value);
      closeSemesterDialog();



    } catch (error) {
      console.error("Error fetching schedule:", error);
    }
  } else {
    // Handle error, display a message or prevent further action
    console.error("Please select one group and one semester");
  }
};


</script>


<style>
  .mt-10 {
    margin-top: 10px;
  }
</style>
