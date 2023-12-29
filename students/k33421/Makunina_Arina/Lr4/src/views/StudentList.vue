<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="elevation-12">
          <v-toolbar color="teal" dark>
            <v-toolbar-title class="text-uppercase font-weight-bold">Student Details</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-list-item three-line>
                  <v-list-item-content>
                    <v-list-item-title class="headline">{{ student ? student.name : 'Loading...' }}</v-list-item-title>
                    <v-list-item-subtitle>{{ student ? student.group.name : '' }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>

                <v-subheader class="mt-4 mb-2">Grades:</v-subheader>
                <v-list dense>
                  <v-list-item v-if="student?.grades" v-for="grade in student.grades" :key="grade.id" two-line>
                    <v-list-item-content>
                      <v-list-item-title>{{ getDisciplineName(grade.schedule.discipline.id) }}</v-list-item-title>
                      <v-list-item-subtitle>Grade: {{ grade.grade }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-else>
                    <v-list-item-content>
                      <v-list-item-title>No grades available</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      student: null,
      disciplines: {}, // Store discipline names for reference
    };
  },
  mounted() {
    const studentId = 1; // Replace with the actual student ID
    const apiUrl = `http://localhost:8000/journal/students/${studentId}/`;

    axios.get(apiUrl)
      .then(response => {
        this.student = response.data;
        // Fetch discipline names and store them in the 'disciplines' object
        this.fetchDisciplineNames();
      })
      .catch(error => {
        console.error('Error fetching student data:', error);
      });
  },
  methods: {
    async fetchDisciplineNames() {
      try {
        const response = await axios.get('http://localhost:8000/journal/disciplines/');
        const disciplines = response.data.reduce((acc, discipline) => {
          acc[discipline.id] = discipline.name;
          return acc;
        }, {});
        this.disciplines = disciplines;
      } catch (error) {
        console.error('Error fetching discipline names:', error);
      }
    },
    getDisciplineName(disciplineId) {
      return this.disciplines[disciplineId] || 'Unknown Discipline';
    },
  },
};
</script>
