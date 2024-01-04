<template>
  <v-container>
    <v-list>
      <v-list-item
        v-for="(teacher, index) in teachers"
        :key="index"
        :title="'Фамилия и имя: ' + teacher.name"
        :subtitle="'Номер аудитории: ' + teacher.room__number"
      >
        <v-list-item-action>
          <v-btn color="error" @click="deleteTeacher(teacher.id)">
            Удалить
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>

    <v-form @submit.prevent="addTeacher">
      <v-text-field v-model="newTeacherName" label="Фамилия и Имя"></v-text-field>
      <v-btn type="submit">Добавить</v-btn>
    </v-form>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {fetchWrapper} from "@/helpers";

const baseUrl = `${import.meta.env.VITE_API_URL}`;

const teachers = ref([])
const newTeacherName = ref('')

const fetchTeachers = async () => {
  const response = await fetchWrapper.get(`${baseUrl}/teachers/`)
  teachers.value = response.teachers
}

const deleteTeacher = async (id) => {
  await fetchWrapper.delete(`${baseUrl}/teacher/?id=${id}`)
  await fetchTeachers()
}

const addTeacher = async () => {
  await fetchWrapper.post(`${baseUrl}/teacher/`, { name: newTeacherName.value })
  newTeacherName.value = ''
  await fetchTeachers()
}

onMounted(fetchTeachers)
</script>
