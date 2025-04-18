import { useToast } from 'primevue/usetoast';

export function useToastService() {
  const toast = useToast();

  function showError(detail, summary = 'Error') {
    toast.add({
      severity: 'error',
      summary,
      detail,
      life: 3000
    });
  }

  function showWarning(detail, summary = 'Warning') {
    toast.add({
      severity: 'warn',
      summary,
      detail,
      life: 3000
    });
  }

  function showSuccess(detail, summary = 'Success') {
    toast.add({
      severity: 'success',
      summary,
      detail,
      life: 3000
    });
  }

  return {
    showError,
    showWarning,
    showSuccess
  };
}