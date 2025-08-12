import { createRouter, createWebHistory } from 'vue-router'
import { authStore } from '@/stores/auth'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('@/views/public/HomeView.vue'),
        },

        {
            path: '/login',
            name: 'login',
            component: () => import('@/views/public/LoginView.vue'),
        },

        {
            path: '/sair',
            name: 'logout',
            component: () => import('@/views/public/LogoutView.vue'),
        },

        {
            path: '/painel',
            name: 'dashboard',
            component: () => import('@/views/private/DashboardView.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: '/401',
            name: 'unauthorized',
            component: () => import('@/views/error/UnauthorizedView.vue'),
            props: (route) => ({
                error: route.query.error,
            }),
            meta: { renderMenu: false },
        },
        {
            path: '/403',
            name: 'forbidden',
            component: () => import('@/views/error/ForbiddenView.vue'),
            meta: { renderMenu: false },
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'NotFound',
            component: () => import('@/views/error/NotFoundView.vue'),
            meta: { renderMenu: false },
        },
    ],
})

router.beforeEach(async (to) => {
    if (to.meta.requiresAuth) {
        const auth = authStore()

        await auth.validateToken().catch(() => {
            auth.logout()
            return router.push({ name: 'forbidden' })
        })

        await auth.fetchUserInfo()

        if (auth.userInfo?.isStaff === true) {
            window.location.href = '/admin/'
        }
    }
})

export default router
