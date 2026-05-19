import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createMemoryHistory } from 'vue-router';
import NutritionCheckPage from '@/views/NutritionCheckPage.vue';

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: { template: '<div />' } },
    { path: '/nutrition-check', component: NutritionCheckPage },
    { path: '/nutrition-insights', component: { template: '<div />' } },
    { path: '/profile-summary', component: { template: '<div />' } },
  ],
});

function mountPage() {
  return mount(NutritionCheckPage, {
    global: {
      plugins: [createPinia(), router],
      stubs: { ArrowLeft: true, Check: true, ClipboardCheck: true, Apple: true, Droplet: true, Cookie: true, Carrot: true },
    },
  });
}

describe('NutritionCheckPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('renders the first question on mount', () => {
    const wrapper = mountPage();
    expect(wrapper.text()).toContain('fruits and vegetables');
  });

  it('shows question 1 of 4 in progress indicator', () => {
    const wrapper = mountPage();
    expect(wrapper.text()).toContain('Question 1 of 4');
  });

  it('progress bar has correct role and aria attributes', () => {
    const wrapper = mountPage();
    const bar = wrapper.find('[role="progressbar"]');
    expect(bar.exists()).toBe(true);
    expect(bar.attributes('aria-valuenow')).toBe('1');
    expect(bar.attributes('aria-valuemin')).toBe('1');
    expect(bar.attributes('aria-valuemax')).toBe('4');
  });

  it('selects an answer when option button is clicked', async () => {
    const wrapper = mountPage();
    const options = wrapper.findAll('button[aria-pressed]');
    await options[0].trigger('click');
    expect(options[0].attributes('aria-pressed')).toBe('true');
  });

  it('Next Question button is disabled before an answer is selected', () => {
    const wrapper = mountPage();
    const nextBtn = wrapper.find('button:not([aria-pressed])');
    // Find the Next Question button specifically
    const allButtons = wrapper.findAll('button');
    const nextQuestion = allButtons.find(b => b.text().includes('Next Question'));
    expect(nextQuestion.attributes('disabled')).toBeDefined();
  });

  it('advances to question 2 after selecting an answer and clicking Next', async () => {
    const wrapper = mountPage();
    const options = wrapper.findAll('button[aria-pressed]');
    await options[0].trigger('click');
    const allButtons = wrapper.findAll('button');
    const nextBtn = allButtons.find(b => b.text().includes('Next Question'));
    await nextBtn.trigger('click');
    expect(wrapper.text()).toContain('Question 2 of 4');
  });

  it('shows Previous button on question 2', async () => {
    const wrapper = mountPage();
    const options = wrapper.findAll('button[aria-pressed]');
    await options[0].trigger('click');
    const allButtons = wrapper.findAll('button');
    const nextBtn = allButtons.find(b => b.text().includes('Next Question'));
    await nextBtn.trigger('click');
    expect(wrapper.text()).toContain('Previous');
  });

  it('goes back to question 1 when Previous is clicked', async () => {
    const wrapper = mountPage();
    // Answer Q1
    const options = wrapper.findAll('button[aria-pressed]');
    await options[0].trigger('click');
    const allButtons = wrapper.findAll('button');
    const nextBtn = allButtons.find(b => b.text().includes('Next Question'));
    await nextBtn.trigger('click');
    // Click Previous
    const prevBtn = wrapper.findAll('button').find(b => b.text().includes('Previous'));
    await prevBtn.trigger('click');
    expect(wrapper.text()).toContain('Question 1 of 4');
  });

  it('shows Complete Check button on last question', async () => {
    const wrapper = mountPage();
    // Answer all 4 questions
    for (let i = 0; i < 3; i++) {
      const options = wrapper.findAll('button[aria-pressed]');
      await options[0].trigger('click');
      const allButtons = wrapper.findAll('button');
      const nextBtn = allButtons.find(b => b.text().includes('Next Question'));
      await nextBtn.trigger('click');
    }
    expect(wrapper.text()).toContain('Complete Check');
  });
});
