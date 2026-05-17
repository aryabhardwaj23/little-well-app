<template>
  <div class="min-h-screen bg-white">
    <!-- Hero Section -->
    <section class="relative bg-[#FAF9F6] pt-10 pb-8 md:pt-20 md:pb-12">
      <div class="container relative z-10 mx-auto max-w-6xl px-4 sm:px-6">
        <div class="grid md:grid-cols-2 gap-8 md:gap-12 items-center">
          <!-- Left Content -->
          <div>
            <h1 class="mb-5 text-2xl leading-relaxed text-[#2C5F2D] sm:text-3xl md:mb-6 md:text-4xl">
              Helping families plan healthier lunchboxes with confidence
            </h1>

            <div class="space-y-3 md:space-y-4 text-base md:text-lg text-muted-foreground leading-relaxed">
              <p>
                LittleHelp is a family-focused nutrition planning platform designed to help parents and caregivers make easier, more confident food choices for children.
              </p>
              <p>
                We turn nutrition considerations such as age, allergies, dietary needs, and seasonal ingredients into practical lunchbox ideas that fit everyday routines.
              </p>
            </div>

            <!-- Trust / Value Strip -->
            <div class="mt-5 grid w-full grid-cols-2 gap-x-4 gap-y-4 md:mt-6 md:grid-cols-4 md:gap-x-5 md:gap-y-4">
              <div class="text-left">
                <p class="text-base font-semibold text-[#2C5F2D] md:text-lg">5 to 12</p>
                <p class="text-xs text-muted-foreground">Child age range</p>
              </div>

              <div class="text-left md:-translate-x-3 lg:-translate-x-4">
                <p class="text-base font-semibold text-[#2C5F2D] md:text-lg">Personalised</p>
                <p class="text-xs text-muted-foreground">Age and needs based</p>
              </div>

              <div class="text-left">
                <p class="text-base font-semibold text-[#2C5F2D] md:text-lg">Seasonal</p>
                <p class="text-xs text-muted-foreground">Fresh food guidance</p>
              </div>

              <div class="text-left">
                <p class="text-base font-semibold text-[#2C5F2D] md:text-lg">Practical</p>
                <p class="text-xs text-muted-foreground">Built for busy routines</p>
              </div>
            </div>
          </div>

          <!-- Right Image -->
          <div class="relative">
            <div class="relative rounded-3xl overflow-hidden shadow-xl bg-white p-2">
              <img
                src="https://images.unsplash.com/photo-1627896067004-38a36f39e506?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwYXJlbnQlMjBzaG9wcGluZyUyMGZyZXNoJTIwdmVnZXRhYmxlcyUyMGdyb2Nlcnl8ZW58MXx8fHwxNzc1MDE4Njk1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                alt="Parent choosing fresh vegetables"
                class="w-full h-[260px] sm:h-[340px] md:h-[420px] object-cover rounded-2xl"
              />
            </div>

            <div class="hidden md:block absolute -top-6 -right-6 w-28 h-28 bg-[#A8D5BA]/30 rounded-full -z-10"></div>
            <div class="hidden md:block absolute -bottom-8 right-12 w-20 h-20 bg-[#F7B267]/30 rounded-full -z-10"></div>
          </div>
        </div>
      </div>

      <div
        class="pointer-events-none absolute inset-x-0 bottom-0 z-[1] h-20 bg-gradient-to-b from-transparent via-[#FAF9F6]/60 to-white md:h-28"
        aria-hidden="true"
      />
    </section>

    <!-- What We Offer -->
    <section class="overflow-visible bg-white pb-12 pt-14 md:pb-20 md:pt-20">
      <div class="container mx-auto max-w-6xl overflow-visible px-4 sm:px-6">
        <div class="max-w-3xl mb-8 md:mb-12">
          <h2 class="text-2xl sm:text-3xl md:text-4xl mb-4 text-[#2C5F2D]">
            What LittleHelp offers
          </h2>
          <p class="text-base md:text-lg text-muted-foreground leading-relaxed">
            LittleHelp brings together nutrition guidance, child preferences, allergy awareness, and meal planning tools in one simple experience.
          </p>
        </div>

        <div class="grid gap-5 pb-2 md:grid-cols-3 md:gap-6 md:pb-4">
          <div
            v-for="card in offerCards"
            :key="card.title"
            class="group relative"
          >
            <div
              tabindex="0"
              class="rounded-2xl border border-gray-100 bg-[#FAF9F6] px-5 py-3 shadow-sm transition-shadow hover:shadow-md md:px-6 md:py-4"
            >
              <h3 class="text-center text-base font-semibold text-[#2C5F2D] md:text-lg">
                {{ card.title }}
              </h3>
            </div>
            <div
              role="tooltip"
              class="pointer-events-none absolute left-0 right-0 top-full z-20 mt-3 hidden rounded-xl border border-[#A8D5BA]/40 bg-white p-4 text-left text-sm leading-relaxed text-muted-foreground shadow-lg opacity-0 transition-all duration-200 translate-y-1 group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:translate-y-0 group-focus-within:opacity-100 md:block"
            >
              {{ card.hint }}
            </div>
            <p class="mt-2 text-xs leading-relaxed text-muted-foreground md:hidden">
              {{ card.hint }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Helps -->
    <section class="relative overflow-hidden py-12 md:py-20">
      <div class="pointer-events-none absolute inset-0 z-0 overflow-hidden" aria-hidden="true">
        <div class="absolute inset-0 bg-[#FAF9F6]"></div>
        <div
          class="absolute inset-0 bg-center bg-cover opacity-35 md:opacity-50"
          style="background-image: url('https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1600');"
        ></div>
        <div
          class="absolute inset-y-0 left-0 z-[1] w-[28%] max-w-xs bg-gradient-to-r from-white from-5% via-white/95 via-60% to-transparent sm:w-[32%] sm:max-w-sm"
        ></div>
        <div
          class="absolute inset-y-0 right-0 z-[1] w-[28%] max-w-xs bg-gradient-to-l from-white from-5% via-white/95 via-60% to-transparent sm:w-[32%] sm:max-w-sm"
        ></div>
      </div>

      <div class="container relative z-10 mx-auto max-w-6xl px-4 sm:px-6">
        <div class="rounded-3xl border border-[#E8E4DC] bg-white/95 p-6 shadow-sm backdrop-blur-sm md:p-10">
          <div class="grid items-start gap-8 lg:grid-cols-2 md:gap-12">
            <div>
              <h2 class="mb-5 text-2xl text-[#2C5F2D] sm:text-3xl md:text-4xl">
                Built for real family routines
              </h2>
              <p class="mb-6 text-base leading-relaxed text-muted-foreground md:mb-8 md:text-lg">
                Healthy eating advice can be hard to apply when mornings are busy. LittleHelp focuses on practical, realistic lunchbox support that parents can use quickly.
              </p>

              <div class="rounded-2xl bg-[#FAF9F6] p-5 md:p-6">
                <p class="text-base leading-relaxed text-muted-foreground md:text-lg">
                  Our goal is not to overwhelm families with information, but to help them make
                  <strong class="text-[#2C5F2D]"> confident, realistic, and repeatable choices</strong>.
                </p>
              </div>
            </div>

            <div class="space-y-5 rounded-2xl bg-[#FAF9F6] p-5 md:space-y-6 md:p-6">
              <div>
                <h4 class="mb-1 text-base font-semibold text-gray-800 md:text-lg">Start with each child's needs</h4>
                <p class="text-sm text-muted-foreground md:text-base">
                  Add age band, allergies, dietary restrictions, and nutrition focus areas to guide personalised recommendations.
                </p>
              </div>

              <div>
                <h4 class="mb-1 text-base font-semibold text-gray-800 md:text-lg">Generate lunchbox options</h4>
                <p class="text-sm text-muted-foreground md:text-base">
                  Receive food combinations and recipe inspiration that are easier to understand and prepare.
                </p>
              </div>

              <div>
                <h4 class="mb-1 text-base font-semibold text-gray-800 md:text-lg">Understand the reason behind choices</h4>
                <p class="text-sm text-muted-foreground md:text-base">
                  See simple explanations that connect food suggestions to nutrition needs and family preferences.
                </p>
              </div>

              <div>
                <h4 class="mb-1 text-base font-semibold text-gray-800 md:text-lg">Save and reuse weekly plans</h4>
                <p class="text-sm text-muted-foreground md:text-base">
                  Keep useful weekly lunchbox plans so future preparation becomes faster and more consistent.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Principles -->
    <section class="py-12 md:py-20 bg-white">
      <div class="container mx-auto px-4 sm:px-6 max-w-6xl">
        <div class="max-w-3xl mb-8 md:mb-12">
          <h2 class="text-2xl sm:text-3xl md:text-4xl mb-4 text-[#2C5F2D]">Our principles</h2>
          <p class="text-base md:text-lg text-muted-foreground leading-relaxed">
            LittleHelp is designed around clarity, practicality, and trust.
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-5 md:gap-6">
          <div class="border-l-4 border-[#A8D5BA] py-2 pl-5 md:pl-6">
            <h3 class="text-lg md:text-xl font-semibold text-[#2C5F2D] mb-3">Simple</h3>
            <p class="text-muted-foreground leading-relaxed">
              Information should be easy to understand and simple enough to act on.
            </p>
          </div>

          <div class="border-l-4 border-[#F7B267] py-2 pl-5 md:pl-6">
            <h3 class="text-lg md:text-xl font-semibold text-[#8B4513] mb-3">Practical</h3>
            <p class="text-muted-foreground leading-relaxed">
              Recommendations should fit into real shopping, cooking, and lunch-packing routines.
            </p>
          </div>

          <div class="border-l-4 border-[#CDE7F0] py-2 pl-5 md:pl-6">
            <h3 class="text-lg md:text-xl font-semibold text-[#1B4965] mb-3">Supportive</h3>
            <p class="text-muted-foreground leading-relaxed">
              The experience should guide families gently, without guilt, pressure, or unrealistic expectations.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Privacy Section -->
    <section class="py-12 md:py-20 bg-[#FAF9F6]">
      <div class="container mx-auto px-4 sm:px-6 max-w-6xl">
        <h2 class="text-2xl md:text-3xl mb-4 text-[#2C5F2D]">Privacy and trust</h2>
        <p class="mb-5 max-w-3xl text-base leading-relaxed text-muted-foreground md:text-lg">
          LittleHelp is built to minimise unnecessary personal information. Families can use nicknames for child profiles, and the platform focuses only on the details needed to provide better lunchbox guidance.
        </p>

        <div class="grid sm:grid-cols-3 gap-4">
              <div class="rounded-xl bg-white p-4">
                <p class="font-semibold text-[#2C5F2D] mb-1">Profile control</p>
                <p class="text-sm text-muted-foreground">Create, edit, or delete child profiles.</p>
              </div>

              <div class="rounded-xl bg-white p-4">
                <p class="font-semibold text-[#2C5F2D] mb-1">Minimal details</p>
                <p class="text-sm text-muted-foreground">Only use information relevant to lunchbox planning.</p>
              </div>

              <div class="rounded-xl bg-white p-4">
                <p class="font-semibold text-[#2C5F2D] mb-1">Clear purpose</p>
                <p class="text-sm text-muted-foreground">Information is used to support personalised recommendations.</p>
              </div>
        </div>
      </div>
    </section>

    <!-- Data Sources Section -->
    <section id="data-sources" class="scroll-mt-24 py-12 md:py-20 bg-white">
      <div class="container mx-auto px-4 sm:px-6 max-w-6xl">
        <div class="max-w-3xl mb-8 md:mb-12">
          <p class="text-sm font-semibold uppercase tracking-wide text-[#2C5F2D] mb-3">
            Data & attribution
          </p>

          <h2 class="text-2xl sm:text-3xl md:text-4xl mb-4 text-[#2C5F2D]">
            Public data sources behind LittleHelp
          </h2>

          <p class="text-base md:text-lg text-muted-foreground leading-relaxed">
            LittleHelp uses public food, nutrition, allergen, and seasonal food references to support educational lunchbox planning. These sources help us connect child profiles with practical serving guidance, packaged food awareness, and seasonal ingredient suggestions.
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div class="rounded-2xl border border-[#D6E7DC] bg-[#FAF9F6] p-5">
            <p class="text-sm font-semibold text-[#2C5F2D]">Packaged food data</p>
            <p class="mt-2 text-sm text-muted-foreground leading-relaxed">
              OpenFoodFacts supports packaged food, label, allergen, and additive-related information.
            </p>
          </div>

          <div class="rounded-2xl border border-[#D6E7DC] bg-[#FAF9F6] p-5">
            <p class="text-sm font-semibold text-[#2C5F2D]">Nutrition references</p>
            <p class="mt-2 text-sm text-muted-foreground leading-relaxed">
              AUSNUT and Australian Dietary Guidelines support food group and serving size guidance.
            </p>
          </div>

          <div class="rounded-2xl border border-[#D6E7DC] bg-[#FAF9F6] p-5">
            <p class="text-sm font-semibold text-[#2C5F2D]">Allergen matching</p>
            <p class="mt-2 text-sm text-muted-foreground leading-relaxed">
              OpenFoodFacts allergen taxonomy helps standardise allergen names and matching.
            </p>
          </div>

          <div class="rounded-2xl border border-[#D6E7DC] bg-[#FAF9F6] p-5">
            <p class="text-sm font-semibold text-[#2C5F2D]">Seasonal food guidance</p>
            <p class="mt-2 text-sm text-muted-foreground leading-relaxed">
              Seasonal food resources support fresh ingredient suggestions for Australian families.
            </p>
          </div>
        </div>

        <div class="overflow-x-auto rounded-2xl border border-[#E5E7EB] bg-white shadow-sm">
          <table class="w-full min-w-[920px] text-sm">
            <thead>
              <tr class="bg-[#FAF9F6] text-left text-[#374151]">
                <th class="px-4 py-3 font-semibold">ID</th>
                <th class="px-4 py-3 font-semibold">Data source</th>
                <th class="px-4 py-3 font-semibold">Purpose in LittleHelp</th>
                <th class="px-4 py-3 font-semibold">Format</th>
                <th class="px-4 py-3 font-semibold">Update method</th>
                <th class="px-4 py-3 font-semibold">Licence / attribution</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="source in dataSources"
                :key="source.id"
                class="border-t border-[#E5E7EB]"
              >
                <td class="px-4 py-4 font-semibold text-[#2C5F2D] align-top">
                  {{ source.id }}
                </td>

                <td class="px-4 py-4 align-top">
                  <a
                    :href="source.link"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="font-semibold text-[#2C5F2D] hover:underline"
                  >
                    {{ source.name }}
                  </a>
                </td>

                <td class="px-4 py-4 text-muted-foreground leading-relaxed align-top">
                  {{ source.purpose }}
                </td>

                <td class="px-4 py-4 align-top">
                  <span class="rounded-full bg-[#F8F5EC] border border-[#E8E4DC] px-3 py-1 text-xs text-[#2C5F2D]">
                    {{ source.format }}
                  </span>
                </td>

                <td class="px-4 py-4 text-muted-foreground align-top">
                  {{ source.updateMethod }}
                </td>

                <td class="px-4 py-4 text-muted-foreground align-top">
                  {{ source.licence }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <p class="mt-4 text-xs text-muted-foreground leading-relaxed">
          Data sources are used for educational planning support only. LittleHelp does not provide medical advice, and source licences should be reviewed before redistribution or commercial reuse.
        </p>
      </div>
    </section>

    <!-- Mission / CTA -->
    <section class="relative overflow-hidden py-12 md:py-20">
      <div
        class="absolute inset-0 bg-gradient-to-br from-[#A8D5BA]/15 to-white"
        aria-hidden="true"
      ></div>
      <div
        class="pointer-events-none absolute inset-x-0 top-0 z-[1] h-48 bg-gradient-to-b from-white from-0% via-white/90 via-[58%] to-transparent to-100% sm:h-56 md:h-64"
        aria-hidden="true"
      ></div>
      <div class="container relative z-10 mx-auto max-w-4xl px-4 text-center sm:px-6">
        <img
          :src="logoUrl"
          alt="LittleHelp logo"
          class="h-14 md:h-20 w-auto object-contain mx-auto mb-6"
        />

        <h2 class="text-2xl sm:text-3xl md:text-4xl mb-5 md:mb-6 text-[#2C5F2D]">Our mission</h2>

        <p class="text-base md:text-xl text-muted-foreground leading-relaxed mb-8 md:mb-10 max-w-2xl mx-auto">
          To help families turn nutrition knowledge into simple, practical lunchboxes that children can enjoy and parents can prepare with confidence.
        </p>

        <button
          @click="goToStartPlanning"
          type="button"
          class="w-full sm:w-auto bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-xl px-8 md:px-10 py-4 text-base md:text-lg font-semibold transition-colors shadow-sm"
        >
          Start Planning Lunchboxes
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import logoUrl from '../assets/littlehelp-logo.jpg';

const router = useRouter();

const offerCards = [
  {
    title: 'Family-focused planning',
    hint: 'Create child profiles and receive lunchbox ideas that consider age, allergies, dietary restrictions, and nutrition focus areas.',
  },
  {
    title: 'Balanced lunchbox ideas',
    hint: 'Build practical lunchboxes with a mix of protein, grains, fruit, vegetables, and child-friendly options.',
  },
  {
    title: 'Weekly meal planning',
    hint: 'Plan multiple days at once, choose how often to cook, and save weekly lunchbox plans for easier school-week preparation.',
  },
  {
    title: 'Simple nutrition guidance',
    hint: 'Understand food choices through clear explanations, without overwhelming nutrition jargon or strict dieting rules.',
  },
  {
    title: 'Seasonal suggestions',
    hint: 'Receive practical suggestions that highlight seasonal produce and everyday ingredients suitable for lunchboxes.',
  },
  {
    title: 'Privacy-conscious design',
    hint: 'LittleHelp is designed to work with minimal personal details. Families can use nicknames and manage profiles with privacy in mind.',
  },
];


const dataSources = [
  {
    id: 'D01',
    name: 'OpenFoodFacts',
    link: 'https://world.openfoodfacts.org/data',
    purpose: 'Packaged food product data, labels, allergens, and additive-related information.',
    format: 'CSV',
    updateMethod: 'Re-downloaded and reloaded at each iteration',
    licence: 'Open Database License (ODbL)',
  },
  {
    id: 'D02',
    name: 'AUSNUT 2023 ? Australian Dietary Guidelines Classification System',
    link: 'https://www.foodstandards.gov.au/science-data/food-nutrient-databases/ausnut/data-files',
    purpose: 'Maps foods to Australian Dietary Guidelines classification categories.',
    format: 'XLSX',
    updateMethod: 'Static; 2023 is the latest public release used',
    licence: 'Creative Commons Attribution 4.0',
  },
  {
    id: 'D03',
    name: 'AUSNUT 2023 ? Food Details',
    link: 'https://www.foodstandards.gov.au/science-data/food-nutrient-databases/ausnut/data-files',
    purpose: 'Food names, descriptions, and nutrition-related reference data.',
    format: 'XLSX',
    updateMethod: 'Static; 2023 is the latest public release used',
    licence: 'Creative Commons Attribution 4.0',
  },
  {
    id: 'D04',
    name: 'AUSNUT Release 3 ? Food Group Information',
    link: 'https://www.foodstandards.gov.au/science-data/food-nutrient-databases/afcd/data-files',
    purpose: 'Food group classification support for matching foods to broader groups.',
    format: 'XLSX',
    updateMethod: 'Static / historical release',
    licence: 'Creative Commons Attribution 4.0',
  },
  {
    id: 'D05',
    name: 'Australian Dietary Guidelines ? Recommended Serves for Children',
    link: 'https://www.eatforhealth.gov.au/food-essentials/how-much-do-we-need-each-day/recommended-number-serves-children-adolescents-and-toddlers',
    purpose: 'Age-based serving size reference for children and adolescents.',
    format: 'PDF / Web',
    updateMethod: 'Static in current project release',
    licence: 'Creative Commons Attribution 4.0',
  },
  {
    id: 'D06',
    name: 'OpenFoodFacts Allergens Taxonomy',
    link: 'https://github.com/openfoodfacts/openfoodfacts-server/blob/main/taxonomies/allergens.txt',
    purpose: 'Allergen name standardisation and allergen matching.',
    format: 'TXT',
    updateMethod: 'Re-downloaded and reloaded at each iteration',
    licence: 'Open Database License (ODbL)',
  },
  {
    id: 'D07',
    name: 'Eating Green: The Environment Victoria Guide to Seasonal Food',
    link: 'https://environmentvictoria.org.au/wp-content/uploads/2016/06/seasonal-food-calendar.pdf',
    purpose: 'Seasonal ingredient guidance for Australian food planning.',
    format: 'PDF',
    updateMethod: 'Static',
    licence: 'Check source licence / attribution required',
  },
];

const goToStartPlanning = () => {
  router.push('/child-profile');
};

</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>
