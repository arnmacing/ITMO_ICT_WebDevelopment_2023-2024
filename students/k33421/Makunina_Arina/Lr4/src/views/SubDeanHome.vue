<template>
  <v-container class="mt-10">
    <v-row justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title>Преподаватели</v-card-title>
          <v-card-actions>
            <v-btn text color="primary" @click="goToTeachers">Перейти</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title>Учебные группы</v-card-title>
          <v-card-actions>
            <v-btn text color="primary" @click="goToGroups">Перейти</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title>Студенты</v-card-title>
          <v-card-actions>
            <v-btn text color="primary" @click="goToStudents">Перейти</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToTeachers = () => {
  router.push('/teachers')
}

const goToGroups = () => {
  router.push('/groups')
}

const goToStudents = () => {
  router.push('/students')
}
</script>

<style>
  .mt-10 {
    margin-top: 10px;
  }
</style>
