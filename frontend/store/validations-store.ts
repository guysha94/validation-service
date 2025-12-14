import {create} from 'zustand'
import {immer} from 'zustand/middleware/immer'

type State = {

    addFormOpen: boolean;
    currentEvent: { id: string, type: string, label: string } | null | undefined;
}

type Actions = {
    toggleAddFormOpen: () => void;
    setCurrentEvent: (eventType: { id: string, type: string, label: string } | null | undefined) => void;
}

type Store = State & Actions;

const initialState: State = {
    addFormOpen: false,
    currentEvent: null,
}

export const useValidationsStore = create<Store>()(
    immer((set) => ({
        ...initialState,
        toggleAddFormOpen: () =>
            set((state) => {
                state.addFormOpen = !state.addFormOpen
            }),
        setCurrentEvent: (eventType: { id: string, type: string, label: string } | null | undefined) =>
            set((state) => {
                state.currentEvent = eventType
            }),

    })),
)