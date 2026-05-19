import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createMemoryHistory } from 'vue-router';
import ChildInfoPage from '@/views/ChildInfoPage.vue';

// Mock the API so no real HTTP calls happen
vi.mock('@/services/api', () => ({
  getChildById: vi.fn(),
}));

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: { template: '<div />' } },
    { path: '/child-info', component: ChildInfoPage },
    { path: '/child-profile', component: { template: '<div />' } },
    { path: '/nutrition-needs', component: { template: '<div />' } },
  ],
});

function mountPage() {
  return mount(ChildInfoPage, {
    global: {
      plugins: [createPinia(), router],
      stubs: { ArrowLeft: true },
    },
  });
}

describe('ChildInfoPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
  });

  it('renders the page heading', () => {
    const wrapper = mountPage();
    expect(wrapper.text()).toContain('Tell Us About Your Child');
  });

  it('renders all three age group buttons', () => {
    const wrapper = mountPage();
    expect(wrapper.text()).toContain('5-6 years');
    expect(wrapper.text()).toContain('7-9 years');
    expect(wrapper.text()).toContain('10-12 years');
  });

  it('renders all 8 allergy buttons', () => {
    const wrapper = mountPage();
    const allergyButtons = wrapper.findAll('button[aria-pressed]').filter(b =>
      ['Peanuts', 'Tree nuts', 'Milk', 'Eggs', 'Wheat', 'Soy', 'Fish', 'Shellfish']
        .includes(b.text())
    );
    expect(allergyButtons.length).toBe(8);
  });

  it('Continue button is disabled when name and age are empty', () => {
    const wrapper = mountPage();
    const continueBtn = wrapper.findAll('button').find(b =>
      b.text().includes('Continue to Nutrition Focus')
    );
    expect(continueBtn.attributes('disabled')).toBeDefined();
  });

  it('selects an age group when button is clicked', async () => {
    const wrapper = mountPage();
    const ageButtons = wrapper.findAll('button[aria-pressed]').filter(b =>
      ['5-6 years', '7-9 years', '10-12 years'].includes(b.text())
    );
    await ageButtons[0].trigger('click');
    expect(ageButtons[0].attributes('aria-pressed')).toBe('true');
  });

  it('toggles allergy on and off', async () => {
    const wrapper = mountPage();
    const peanutBtn = wrapper.findAll('button[aria-pressed]').find(b => b.text() === 'Peanuts');
    await peanutBtn.trigger('click');
    expect(peanutBtn.attributes('aria-pressed')).toBe('true');
    await peanutBtn.trigger('click');
    expect(peanutBtn.attributes('aria-pressed')).toBe('false');
  });

  it('can select multiple allergies', async () => {
    const wrapper = mountPage();
    const allergyBtns = wrapper.findAll('button[aria-pressed]').filter(b =>
      ['Peanuts', 'Milk'].includes(b.text())
    );
    for (const btn of allergyBtns) {
      await btn.trigger('click');
    }
    const selected = wrapper.findAll('button[aria-pressed="true"]').filter(b =>
      ['Peanuts', 'Milk'].includes(b.text())
    );
    expect(selected.length).toBe(2);
  });

  it('name input has correct id and label association', () => {
    const wrapper = mountPage();
    const input = wrapper.find('#child-name');
    const label = wrapper.find('label[for="child-name"]');
    expect(input.exists()).toBe(true);
    expect(label.exists()).toBe(true);
  });

  it('dietary restriction select has correct id and label', () => {
    const wrapper = mountPage();
    const select = wrapper.find('#dietary-restriction');
    const label = wrapper.find('label[for="dietary-restriction"]');
    expect(select.exists()).toBe(true);
    expect(label.exists()).toBe(true);
  });

  it('selects activity level', async () => {
    const wrapper = mountPage();
    const activityBtns = wrapper.findAll('button[aria-pressed]').filter(b =>
      ['Light', 'Moderate', 'Active'].some(l => b.text().includes(l))
    );
    await activityBtns[0].trigger('click');
    expect(activityBtns[0].attributes('aria-pressed')).toBe('true');
  });
});
