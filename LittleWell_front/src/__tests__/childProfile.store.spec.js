import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useChildProfileStore } from '@/stores/childProfile';

describe('childProfile store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('has empty draft by default', () => {
    const store = useChildProfileStore();
    expect(store.childProfileDraft).toBeDefined();
  });

  it('updateDraft merges new fields into draft', () => {
    const store = useChildProfileStore();
    store.updateDraft({ name: 'Emma', ageGroup: '7-9 years' });
    expect(store.childProfileDraft.name).toBe('Emma');
    expect(store.childProfileDraft.ageGroup).toBe('7-9 years');
  });

  it('updateDraft does not overwrite unrelated fields', () => {
    const store = useChildProfileStore();
    store.updateDraft({ name: 'Emma', ageGroup: '7-9 years' });
    store.updateDraft({ allergies: ['Peanuts'] });
    expect(store.childProfileDraft.name).toBe('Emma');
    expect(store.childProfileDraft.allergies).toEqual(['Peanuts']);
  });

  it('resetDraft clears the draft', () => {
    const store = useChildProfileStore();
    store.updateDraft({ name: 'Emma', ageGroup: '7-9 years' });
    store.resetDraft();
    expect(store.childProfileDraft.name).toBeFalsy();
  });
});
