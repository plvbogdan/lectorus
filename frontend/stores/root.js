export const useRootStore = defineStore('root', {
    state: () => ({
        modal: ''
    }),
    getters: {
        getModal: (state) => state.modal,
    },
    actions: {
        setModal(modal) {
            this.modal = modal;
        }
    }
})