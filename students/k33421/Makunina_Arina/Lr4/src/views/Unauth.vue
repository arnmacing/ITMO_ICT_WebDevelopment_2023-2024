<template>
    <v-container fluid class="fill-height">
      <v-row align="center" justify="center">
        <v-col cols="12" md="8">
          <v-card class="rounded-lg shadow-md">
            <v-card-title class="text-center">
              <h1 class="text-3xl font-bold text-red-600 mb-6">Access Denied</h1>
            </v-card-title>

            <v-card-text>
              <p class="text-lg">
                You do not have the necessary permissions to access this page.
                Please contact your administrator for assistance.
              </p>
            </v-card-text>

            <v-card-actions>
              <v-btn color="primary" to="/login" class="mx-auto">
                Go to Login
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>

</script>

<style scoped>
.fill-height {
  height: 100%;
}

.text-red-600 {
  color: #e3342f;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}
</style>
