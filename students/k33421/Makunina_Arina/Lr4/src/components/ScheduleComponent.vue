<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Расписание для группы {{ group }} на {{ semester }} семестр</h2>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-btn @click="startCreate" color="primary">Добавить запись</v-btn>
      </v-col>
    </v-row>

  <v-row v-for="(entries, dayOfWeek) in groupedSchedule" :key="dayOfWeek">
    <v-col>
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

        <v-dialog v-model="showCreateModal" persistent max-width="600">
      <v-card>
        <v-card-title class="headline">Добавление новой записи в расписание</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="confirmCreate">
            <v-container>
                    <v-row>
                      <v-col>
                        <v-select
                          v-model="newEntry.time_slot"
                          :items="timeslotsOptions.map(item => item.display)"
                          label="Время"
                          required
                        ></v-select>
                        <v-select
                          v-model="newEntry.room_id"
                          :items="roomOptions"
                          label="Аудитория"
                          required
                        ></v-select>
                        <v-select
                          v-model="newEntry.discipline_id"
                          :items="disciplineOptions"
                          label="Предмет"
                          required
                        ></v-select>
                        <v-select
                          v-model="newEntry.teacher_id"
                          :items="teacherOptions"
                          label="Преподаватель"
                          required
                        ></v-select>
                      </v-col>
                    </v-row>
                  </v-container>

                  <v-card-actions>
                    <v-btn color="green darken-1" type="submit">Добавить</v-btn>
                    <v-btn color="red darken-1" @click="showCreateModal = false">Отмена</v-btn>
                  </v-card-actions>
                </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

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
                  <v-select
                   v-model="editedEntry.time_slot_display"
                   :items="timeslotsOptions.map(item => item.display)"
                   label="Время"
                   required
                  ></v-select>
                  <v-select
                    v-model="editedEntry.room.name"
                    :items="roomOptions"
                    label="Аудитория"
                    required
                  ></v-select>
                  <v-select v-model="editedEntry.discipline.name" :items="disciplineOptions" label="Предмет" required></v-select>
                  <v-select v-model="editedEntry.teacher.name" :items="teacherOptions" label="Преподаватель" required></v-select>
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
      showCreateModal: false,
      newEntry: {
        time_slot_id: null,
        room_id: null,
        discipline_id: null,
        teacher_id: null,
      },
      scheduleIdToEdit: null,
      editedEntry: {
        time_slot_id: null,
        room: { name: '' },
        discipline: { name: '' },
        teacher: { name: '' },
      },
      timeslotsOptions: [],
      roomOptions: [],
      disciplineOptions: [],
      teacherOptions: [],
      availableRooms: [],
    };
  },

computed: {
orderedDaysOfWeek() {
  const daysMapping = {
    'Monday': 'Понедельник',
    'Tuesday': 'Вторник',
    'Wednesday': 'Среда',
    'Thursday': 'Четверг',
    'Friday': 'Пятница',
    'Saturday': 'Суббота',
  };

  const orderedDays = _.orderBy(
    _.uniq(this.schedule.map(entry => daysMapping[entry.time_slot.day_of_week_display])),
    day => Object.keys(daysMapping).indexOf(day)
  );

  console.log('Ordered Days:', orderedDays);

  return orderedDays;
},

groupedSchedule() {
  const grouped = _.groupBy(this.schedule, 'time_slot.day_of_week_display');

  console.log('Grouped Schedule:', grouped);

  return grouped;
},
},


async mounted() {
  this.group = this.$route.query.group;
  this.semester = this.$route.query.semester;

  try {
    await this.fetchSchedule();

    await this.fetchTimeSlotOptions();
    await this.fetchRoomOptions();
    await this.fetchDisciplineOptions();
    await this.fetchTeacherOptions();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
},
  methods: {
    async fetchSchedule() {
      try {
        const data = await fetchWrapper.get(`${baseUrl}/schedule/?group=${this.group}&semester=${this.semester}`);
        console.log('Fetched Schedule Data:', data);
        this.schedule = data.schedule;
      } catch (error) {
        console.error('Error fetching schedule:', error);
        throw error; // Rethrow the error to propagate it up the call stack
      }
    },
    async fetchTimeSlotOptions() {
      try {
        const data = await fetchWrapper.get(`${baseUrl}/time_slots/`);
        console.log('Time Slots Data:', data);
        this.timeslotsOptions = data.time_slots.map(slot => ({
          id: slot.id,
          display: `${slot.day_of_week_display} ${slot.start_time} - ${slot.end_time}`,
        }));
      } catch (error) {
        console.error('Error fetching time slots:', error);
      }
    },
    async fetchRoomOptions() {
      try {
        const data = await fetchWrapper.get(`${baseUrl}/rooms/`);
        this.roomOptions = data.available_rooms.map(room => room.number);
        console.log('Room Options:', this.roomOptions);
      } catch (error) {
        console.error('Error fetching room options:', error);
      }
    },
    async fetchDisciplineOptions() {
      try {
        const data = await fetchWrapper.get(`${baseUrl}/disciplines/`);
        this.disciplineOptions = data.map(discipline => discipline.name);
      } catch (error) {
        console.error('Error fetching discipline options:', error);
      }
    },
    async fetchTeacherOptions() {
      try {
        const data = await fetchWrapper.get(`${baseUrl}/teachers/`);
        this.teacherOptions = data.teachers.map(teacher => teacher.name);
      } catch (error) {
        console.error('Error fetching teacher options:', error);
      }
    },
    startCreate() {
      this.showCreateModal = true;
      this.newEntry = {
        time_slot: null,
        room_id: null,
        discipline_id: null,
        teacher_id: null,
      };
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
    async confirmCreate() {
      try {
        // Найдите выбранный временной слот
        const selectedTimeSlot = this.timeslotsOptions.find(slot => slot.id === this.newEntry.time_slot_id);

        const response = await fetchWrapper.post(`${baseUrl}/schedule/`, {
          semester: this.semester,
          group_name: this.group,
          time_slot_id: this.newEntry.time_slot_id,
          room_id: this.newEntry.room_id,
          discipline_id: this.newEntry.discipline_id,
          teacher_id: this.newEntry.teacher_id,
        });

        if (response.status === 'success') {
          this.newEntry.time_slot = selectedTimeSlot ? selectedTimeSlot.display : '';
          await this.fetchSchedule();
        } else {
          console.error('Failed to create schedule entry:', response);
        }
      } catch (error) {
        console.error('Error creating schedule entry:', error);
      }

      this.showCreateModal = false;
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
     const existingEntry = this.schedule.find(entry => entry.id === scheduleId);
      if (existingEntry) {
        const timeSlotDisplay = this.timeslotsOptions.find(slot => slot.id === existingEntry.time_slot.id)?.display;
        this.editedEntry = {
          time_slot_display: timeSlotDisplay || '',
          room: { name: existingEntry.room.name },
          discipline: { name: existingEntry.discipline.name },
          teacher: { name: existingEntry.teacher.name },
          roomSelectionEnabled: false, // Set to true or false based on your requirements
        };
      }
     this.showEditModal = true;
    },
    async confirmEdit() {
      try {
        const room = await fetchWrapper.get(`${baseUrl}/rooms/?name=${encodeURIComponent(this.editedEntry.room.name)}`);
        const discipline = await fetchWrapper.get(`${baseUrl}/disciplines/?name=${encodeURIComponent(this.editedEntry.discipline.name)}`);
        const teacher = await fetchWrapper.get(`${baseUrl}/teachers/?name=${encodeURIComponent(this.editedEntry.teacher.name)}`);

        if (!room || !discipline || !teacher) {
          console.error('Error fetching foreign key IDs.');
          return;
        }

        const updatedEntry = {
          time_slot_id: this.editedEntry.time_slot_id,
          room_id: room.id,
          discipline_id: discipline.id,
          teacher_id: teacher.id,
        };

        await fetchWrapper.put(`${baseUrl}/schedule/?id=${this.scheduleIdToEdit}`, updatedEntry);
        await this.fetchSchedule();
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
</style>
