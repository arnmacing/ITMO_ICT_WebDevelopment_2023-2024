<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title class="headline">
              Личный кабинет студента
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12">
                  <v-card>
                    <v-card-title>Личная информация</v-card-title>
                    <v-card-text>
                      <v-row>
                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="student.firstName"
                            label="Имя"
                            outlined
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="student.lastName"
                            label="Фамилия"
                            outlined
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="student.group.name"
                            label="Группа"
                            outlined
                            readonly
                          ></v-text-field>
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
  
              <v-row>
                <v-col cols="12">
                  <v-card>
                    <v-card-title>Оценки</v-card-title>
                    <v-card-text>
                      <v-data-table
                        :headers="headers"
                        :items="student.grades"
                        :items-per-page="5"
                        class="elevation-1"
                      >
                        <template v-slot:top>
                          <v-toolbar flat>
                            <v-toolbar-title>Оценки по предметам</v-toolbar-title>
                          </v-toolbar>
                        </template>
                        <template v-slot:item="props">
                          <td>{{ props.item.schedule.discipline.name }}</td>
                          <td>{{ props.item.schedule.teacher.name }}</td>
                          <td>{{ props.item.value }}</td>
                        </template>
                      </v-data-table>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/store';
  
  const authStore = useAuthStore();
  
  const student = ref({
    firstName: '',
    lastName: '',
    group: {
      name: '',
    },
    grades: [],
  });
  
  const headers = [
    { text: 'Предмет', value: 'discipline' },
    { text: 'Преподаватель', value: 'teacher' },
    { text: 'Оценка', value: 'value' },
  ];
  
  onMounted(async () => {
    try {
      // Fetch student information based on the authenticated user
      const response = await fetch(`/journal/students/${authStore.userId}/`);
      const data = await response.json();
      student.value = data;
    } catch (error) {
      console.error('Error fetching student information:', error);
    }
  });
  </script>
  
  <style scoped>
  /* Add any specific styles for this component */
  </style>
  