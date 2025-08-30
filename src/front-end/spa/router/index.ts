import { createRouter, createWebHistory } from 'vue-router'
import { authStore } from '@/stores/auth'
import env from 'env'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        // Public pages

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
            path: '/conta/criar',
            name: 'user-add',
            component: () => import('@/views/public/UserCreateView.vue'),
        },

        {
            path: '/confirmar',
            name: 'confirmation',
            component: () => import('@/views/public/ConfirmationView.vue'),
            props: (route) => ({
                message: route.query.message,
                redirect: route.query.redirect,
            }),
            meta: { renderMenu: false },
        },

        // Private pages

        {
            path: '/email/validacao',
            name: 'email-validation',
            component: () => import('@/views/private/EmailValidationView.vue'),
            meta: { requiresAuth: true, renderMenu: false },
        },

        {
            path: '/estabelecimentos',
            name: 'establishments',
            component: () => import('@/views/private/EstablishmentsListView.vue'),
            meta: { requiresAuth: true },
        },

        {
            path: '/estabelecimento/:establishmentId(\\d+)',
            meta: { requiresAuth: true },
            children: [
                {
                    path: 'painel',
                    name: 'dashboard',
                    component: () => import('@/views/private/DashboardView.vue'),
                    props: true,
                },

                {
                    path: 'produto/adicionar',
                    name: 'product-add',
                    component: () => import('@/views/private/ProductCreateView.vue'),
                    props: true,
                },

                {
                    path: 'funcionario/adicionar',
                    name: 'employee-add',
                    component: () => import('@/views/private/EmployeeCreateView.vue'),
                    props: true,
                },
            ],
        },

        // Erro pages

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
    if (env.DEBUG === false) console.clear()

    if (to.meta.requiresAuth) {
        const auth = authStore()

        if ((await auth.validateToken()) === false) {
            auth.logout()
            return router.push({ name: 'forbidden' })
        }

        await auth.fetchInfo()

        if (!auth.userInfo?.isEmailVerified) {
            const emailValidationLink = router.resolve({ name: 'email-validation' }).path
            if (to.path !== emailValidationLink) router.push({ name: 'email-validation' })
        }

        if (auth.userInfo?.isStaff === true) {
            window.location.href = '/admin/'
        }
    }
})

export default router
