import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores';
import { LoginComponent, RegisterComponent, ScheduleComponent } from "@/components";
import { DispatcherHome, SubDeanHome, TeachersList, Unauth } from "@/views";

const routes = [
  { path: '/login', component: LoginComponent },
  { path: '/register', component: RegisterComponent },
  {
    path: '/',
    component: function () {
      const auth = useAuthStore();

      if (auth.role === "Заместитель декана") {
        return SubDeanHome;
      } else if (auth.role === "Диспетчер") {
        return DispatcherHome;
      } else {
        return Unauth;
      }
    },
  },
  {
    path: '/teachers',
    component: function () {
      const auth = useAuthStore();

      if (auth.role === "Заместитель декана") {
        return TeachersList;
      } else if (auth.role === "Диспетчер") {
        return Unauth;
      } else {
        return Unauth;
      }
    },
  },
  {
    path: '/schedule',
    component: () => {
      if (localStorage.getItem('role') === '"Заместитель декана"') {
        return import('@/views/Unauth.vue');
      } else if (localStorage.getItem('role') === '"Диспетчер"') {
        return import('@/components/ScheduleComponent.vue');
      } else {
        return import('@/views/Unauth.vue');
      }
    }
  }
];

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const authStore = useAuthStore();

  if (authStore.access) {
    await authStore.update_role();
  }

  if (authStore.access && (to.path.startsWith('/login') || to.path.startsWith('/register'))) {
    next({ path: '/' });
  } else if (authRequired && !authStore.access) {
    authStore.returnUrl = to.fullPath;
    next({ path: '/login' });
  } else {
    next();
  }
});
