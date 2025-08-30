export interface UserInfo {
    firstName: string
    lastName: string
    email: string
    isStaff: boolean
    isEmailVerified: boolean
}

export interface LoginDetail {
    username: string
    password: string
    stayConnected?: boolean
}
