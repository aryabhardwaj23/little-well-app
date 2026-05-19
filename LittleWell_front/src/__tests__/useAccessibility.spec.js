import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { nextTick } from 'vue';

describe('useAccessibility', () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove('a11y-large-text', 'a11y-high-contrast');
    vi.resetModules();
  });

  afterEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove('a11y-large-text', 'a11y-high-contrast');
    vi.resetModules();
  });

  it('toggleLargeTextMode switches largeTextMode from false to true', async () => {
    const { useAccessibility } = await import('@/composables/useAccessibility');
    const { largeTextMode, toggleLargeTextMode } = useAccessibility();
    expect(largeTextMode.value).toBe(false);
    toggleLargeTextMode();
    await nextTick();
    expect(largeTextMode.value).toBe(true);
  });

  it('toggleHighContrastMode switches highContrastMode from false to true', async () => {
    const { useAccessibility } = await import('@/composables/useAccessibility');
    const { highContrastMode, toggleHighContrastMode } = useAccessibility();
    expect(highContrastMode.value).toBe(false);
    toggleHighContrastMode();
    await nextTick();
    expect(highContrastMode.value).toBe(true);
  });

  it('toggleLargeTextMode switches back to false on second call', async () => {
    const { useAccessibility } = await import('@/composables/useAccessibility');
    const { largeTextMode, toggleLargeTextMode } = useAccessibility();
    toggleLargeTextMode();
    await nextTick();
    toggleLargeTextMode();
    await nextTick();
    expect(largeTextMode.value).toBe(false);
  });

  it('toggleHighContrastMode switches back to false on second call', async () => {
    const { useAccessibility } = await import('@/composables/useAccessibility');
    const { highContrastMode, toggleHighContrastMode } = useAccessibility();
    toggleHighContrastMode();
    await nextTick();
    toggleHighContrastMode();
    await nextTick();
    expect(highContrastMode.value).toBe(false);
  });

  it('adds a11y-large-text class to html when large text is toggled on', async () => {
    const { useAccessibility } = await import('@/composables/useAccessibility');
    const { toggleLargeTextMode } = useAccessibility();
    toggleLargeTextMode();
    await nextTick();
    expect(document.documentElement.classList.contains('a11y-large-text')).toBe(true);
  });

  it('adds a11y-high-contrast class to html when high contrast is toggled on', async () => {
    const { useAccessibility } = await import('@/composables/useAccessibility');
    const { toggleHighContrastMode } = useAccessibility();
    toggleHighContrastMode();
    await nextTick();
    expect(document.documentElement.classList.contains('a11y-high-contrast')).toBe(true);
  });

  it('persists large text ON to localStorage', async () => {
    const { useAccessibility } = await import('@/composables/useAccessibility');
    const { toggleLargeTextMode } = useAccessibility();
    toggleLargeTextMode();
    await nextTick();
    expect(localStorage.getItem('littlehelp_accessibility_large_text')).toBe('1');
  });

  it('persists large text OFF to localStorage', async () => {
    const { useAccessibility } = await import('@/composables/useAccessibility');
    const { toggleLargeTextMode } = useAccessibility();
    toggleLargeTextMode();
    await nextTick();
    toggleLargeTextMode();
    await nextTick();
    expect(localStorage.getItem('littlehelp_accessibility_large_text')).toBe('0');
  });

  it('persists high contrast ON to localStorage', async () => {
    const { useAccessibility } = await import('@/composables/useAccessibility');
    const { toggleHighContrastMode } = useAccessibility();
    toggleHighContrastMode();
    await nextTick();
    expect(localStorage.getItem('littlehelp_accessibility_high_contrast')).toBe('1');
  });

  it('toggles accessibility menu open and closed', async () => {
    const { useAccessibility } = await import('@/composables/useAccessibility');
    const { showAccessibilityMenu, toggleAccessibilityMenu } = useAccessibility();
    expect(showAccessibilityMenu.value).toBe(false);
    toggleAccessibilityMenu();
    await nextTick();
    expect(showAccessibilityMenu.value).toBe(true);
    toggleAccessibilityMenu();
    await nextTick();
    expect(showAccessibilityMenu.value).toBe(false);
  });
});