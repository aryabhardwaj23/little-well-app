import { ref, watch, onMounted, onBeforeUnmount } from 'vue';

// Shared reactive state — same refs across all components
const largeTextMode = ref(false);
const highContrastMode = ref(false);
let _initialized = false;

const STORAGE_KEY_TEXT = 'littlehelp_accessibility_large_text';
const STORAGE_KEY_CONTRAST = 'littlehelp_accessibility_high_contrast';

function applyToDocument() {
  const root = document.documentElement;
  if (largeTextMode.value) {
    root.classList.add('a11y-large-text');
  } else {
    root.classList.remove('a11y-large-text');
  }
  if (highContrastMode.value) {
    root.classList.add('a11y-high-contrast');
  } else {
    root.classList.remove('a11y-high-contrast');
  }
}

function initFromStorage() {
  if (_initialized) return;
  _initialized = true;
  largeTextMode.value = localStorage.getItem(STORAGE_KEY_TEXT) === '1';
  highContrastMode.value = localStorage.getItem(STORAGE_KEY_CONTRAST) === '1';
  applyToDocument();
}

watch(largeTextMode, () => {
  localStorage.setItem(STORAGE_KEY_TEXT, largeTextMode.value ? '1' : '0');
  applyToDocument();
});

watch(highContrastMode, () => {
  localStorage.setItem(STORAGE_KEY_CONTRAST, highContrastMode.value ? '1' : '0');
  applyToDocument();
});

export function useAccessibility() {
  onMounted(() => {
    initFromStorage();
  });

  function toggleLargeTextMode() {
    largeTextMode.value = !largeTextMode.value;
  }

  function toggleHighContrastMode() {
    highContrastMode.value = !highContrastMode.value;
  }

  // Dropdown open/close with keyboard (Escape) and outside-click support
  const showAccessibilityMenu = ref(false);
  const accessibilityMenuRef = ref(null);

  function toggleAccessibilityMenu() {
    showAccessibilityMenu.value = !showAccessibilityMenu.value;
  }

  function handleDocumentClick(event) {
    if (!showAccessibilityMenu.value) return;
    if (!accessibilityMenuRef.value?.contains(event.target)) {
      showAccessibilityMenu.value = false;
    }
  }

  function handleDocumentKeydown(event) {
    if (event.key === 'Escape' && showAccessibilityMenu.value) {
      showAccessibilityMenu.value = false;
    }
  }

  function mountListeners() {
    document.addEventListener('click', handleDocumentClick);
    document.addEventListener('keydown', handleDocumentKeydown);
  }

  function unmountListeners() {
    document.removeEventListener('click', handleDocumentClick);
    document.removeEventListener('keydown', handleDocumentKeydown);
  }

  onMounted(mountListeners);
  onBeforeUnmount(unmountListeners);

  return {
    largeTextMode,
    highContrastMode,
    showAccessibilityMenu,
    accessibilityMenuRef,
    toggleLargeTextMode,
    toggleHighContrastMode,
    toggleAccessibilityMenu,
  };
}