<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Расписание для группы {{ group }} на {{ semester }} семестр</h2>
      </v-col>
    </v-row>

    <v-row>
      <v-col v-for="dayOfWeek in orderedDaysOfWeek" :key="dayOfWeek">
        <h3>{{ dayOfWeek }}</h3>
        <v-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left" style="width: 20%;">Время</th>
                <th class="text-left" style="width: 20%;">Аудитория</th>
                <th class="text-left" style="width: 20%;">Предмет</th>
                <th class="text-left" style="width: 20%;">Преподаватель</th>
                <th style="width: 10%;"></th>
                <th style="width: 10%;"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="entry in groupedSchedule[dayOfWeek]" :key="entry.id">
                <td style="width: 20%;">{{ entry.time_slot.start_time }} - {{ entry.time_slot.end_time }}</td>
                <td style="width: 20%;">{{ entry.room.name }}</td>
                <td style="width: 20%;">{{ entry.discipline.name }}</td>
                <td style="width: 20%;">{{ entry.teacher.name }}</td>
                <td style="width: 10%;">
                  <v-btn icon @click="startEdit(entry.id)">
                    <v-icon color="blue">mdi-pencil</v-icon>
                  </v-btn>
                </td>
                <td style="width: 10%;">
                  <v-btn icon @click="startDelete(entry.id)">
                    <v-icon color="red">mdi-delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </template>
        </v-table>
      </v-col>
    </v-row>

    <v-dialog v-model="showDeleteConfirm" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Подтверждение</v-card-title>
        <v-card-text>Вы действительно хотите удалить этот элемент расписания?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="showDeleteConfirm = false">Отмена</v-btn>
          <v-btn color="red darken-1" text @click="confirmDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showEditModal" persistent max-width="600">
      <v-card>
        <v-card-title class="headline">Редактирование элемента расписания</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="confirmEdit">
            <v-container>
              <v-row>
                <v-col>
                  <v-text-field v-model="editedEntry.time_slot.day_of_week_display" label="Дата" required></v-text-field>
                  <v-text-field v-model="editedEntry.time_slot.start_time" label="Время начала" required></v-text-field>
                  <v-text-field v-model="editedEntry.time_slot.end_time" label="Время окончания" required></v-text-field>
                  <v-text-field v-model="editedEntry.room.name" label="Аудитория" required></v-text-field>
                  <v-text-field v-model="editedEntry.discipline.name" label="Предмет" required></v-text-field>
                  <v-text-field v-model="editedEntry.teacher.name" label="Преподаватель" required></v-text-field>
                </v-col>
              </v-row>
            </v-container>

            <v-card-actions>
              <v-btn color="green darken-1" type="submit">Сохранить</v-btn>
              <v-btn color="red darken-1" @click="showEditModal = false">Отмена</v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import { fetchWrapper } from "@/helpers";
import _ from 'lodash';

const baseUrl = `${import.meta.env.VITE_API_URL}`;

export default {
  data() {
    return {
      group: null,
      semester: null,
      schedule: [],
      showDeleteConfirm: false,
      scheduleIdToDelete: null,
      showEditModal: false,
      scheduleIdToEdit: null,
      editedEntry: {
        time_slot: {
          day_of_week_display: '',
          start_time: '',
          end_time: '',
        },
        room: { name: '' },
        discipline: { name: '' },
        teacher: { name: '' },
      },
    };
  },
  computed: {
    orderedDaysOfWeek() {
      // Order days of week
      return _.orderBy(_.uniq(this.schedule.map(entry => entry.time_slot.day_of_week_display)));
    },
    groupedSchedule() {
      // Group schedule by day of week
      return _.groupBy(this.schedule, 'time_slot.day_of_week_display');
    },
  },
  mounted() {
    this.group = this.$route.query.group;
    this.semester = this.$route.query.semester;
    this.fetchSchedule();
  },
  methods: {
    async fetchSchedule() {
      try {
        const data = await fetchWrapper.get(`${baseUrl}/schedule/?group=${this.group}&semester=${this.semester}`);
        this.schedule = data.schedule;
      } catch (error) {
        console.error('Error fetching schedule:', error);
      }
    },
    startDelete(scheduleId) {
      this.scheduleIdToDelete = scheduleId;
      this.showDeleteConfirm = true;
    },
    async confirmDelete() {
      await this.deleteSchedule(this.scheduleIdToDelete);
      this.showDeleteConfirm = false;
      this.scheduleIdToDelete = null;
    },
    async deleteSchedule(scheduleId) {
      try {
        await fetchWrapper.delete(`${baseUrl}/schedule/?id=${scheduleId}`);
        this.fetchSchedule();
      } catch (error) {
        console.error('Error deleting schedule entry:', error);
      }
    },
    startEdit(scheduleId) {
      this.scheduleIdToEdit = scheduleId;
      this.showEditModal = true;
      const existingEntry = this.schedule.find(entry => entry.id === scheduleId);
      if (existingEntry) {
        this.editedEntry = { ...existingEntry };
      }
    },
    async confirmEdit() {
      try {
        const room = await fetchWrapper.get(`${baseUrl}/room/?name=${this.editedEntry.room.name}`);
        const discipline = await fetchWrapper.get(`${baseUrl}/discipline/?name=${this.editedEntry.discipline.name}`);
        const teacher = await fetchWrapper.get(`${baseUrl}/teacher/?name=${this.editedEntry.teacher.name}`);

        if (!room || !discipline || !teacher) {
          console.error('Error fetching foreign key IDs.');
          return;
        }

        this.editedEntry.room.id = room.id;
        this.editedEntry.discipline.id = discipline.id;
        this.editedEntry.teacher.id = teacher.id;

        const response = await fetchWrapper.put(`${baseUrl}/schedule/${this.scheduleIdToEdit}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.editedEntry),
        });

        if (response.ok) {
          this.fetchSchedule();
        } else {
          console.error('Error updating schedule entry:', response.statusText);
        }
      } catch (error) {
        console.error('Error updating schedule entry:', error);
      }

      this.showEditModal = false;
      this.scheduleIdToEdit = null;
    },
  },
};
</script>

<style scoped>
/* Добавьте пользовательские стили, если необходимо */
</style>
