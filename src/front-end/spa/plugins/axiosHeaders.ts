import axios from 'axios'

function getCSRFToken(): string | null {
    const input = document.querySelector(
        'input[name=csrfmiddlewaretoken]'
    ) as HTMLInputElement | null

    if (input != null) return input.value

    throw new Error('Csrf token not found')
}

export default {
    install() {
        axios.defaults.headers.common['X-CSRFToken'] = getCSRFToken()
        axios.defaults.headers.common['Content-Type'] = 'multipart/form-data'
    }
}
