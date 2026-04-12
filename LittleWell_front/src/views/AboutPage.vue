<template>
  <div class="min-h-screen bg-white">
    <!-- Navigation Bar -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <div 
            class="flex items-center gap-2 cursor-pointer"
            @click="goToHome"
          >
            <div class="w-10 h-10 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] rounded-full flex items-center justify-center">
              <HeartIcon class="w-5 h-5 text-white" />
            </div>
            <span class="text-xl font-semibold text-[#2C5F2D]">LittleWell</span>
          </div>

          <!-- Back Button -->
          <button
            @click="goToHome"
            class="inline-flex items-center px-4 py-2 text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-lg transition-colors"
          >
            <ArrowLeftIcon class="w-4 h-4 mr-2" />
            Back to Home
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="pt-16">
      <!-- Hero Section -->
      <div class="py-20 bg-[#FAF9F6]">
        <div class="container mx-auto px-6 max-w-6xl">
          <div class="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h1 class="text-4xl md:text-5xl mb-6">About us</h1>
              <div class="space-y-4 text-lg text-muted-foreground leading-relaxed">
                <p>
                  LittleWell is a student-led project developed at <strong class="text-[#2C5F2D]">Monash University</strong>, focused on supporting parents in making better everyday nutrition decisions for their children.
                </p>
                <p>
                  We aim to bridge the gap between complex nutrition information and real-life food choices by turning knowledge into simple, practical guidance.
                </p>
              </div>
            </div>

            <div class="relative">
              <div class="rounded-3xl overflow-hidden shadow-xl">
                <img
                  src="https://images.unsplash.com/photo-1627896067004-38a36f39e506?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwYXJlbnQlMjBzaG9wcGluZyUyMGZyZXNoJTIwdmVnZXRhYmxlcyUyMGdyb2Nlcnl8ZW58MXx8fHwxNzc1MDE4Njk1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                  alt="Parent shopping fresh vegetables"
                  class="w-full h-[400px] object-cover"
                />
              </div>
              <div class="absolute -bottom-6 -right-6 w-32 h-32 bg-[#A8D5BA] rounded-full -z-10"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Key Information Grid -->
      <div class="py-20 bg-white">
        <div class="container mx-auto px-6 max-w-6xl">
          <h2 class="text-3xl mb-12">What we offer</h2>
          
          <div class="grid md:grid-cols-3 gap-6">
            <div class="p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow bg-[#FAF9F6]">
              <div class="w-12 h-12 bg-[#A8D5BA] rounded-full flex items-center justify-center mb-4">
                <UsersIcon class="w-6 h-6 text-[#2C5F2D]" />
              </div>
              <h3 class="text-xl mb-3 text-[#2C5F2D]">Who we are</h3>
              <p class="text-muted-foreground leading-relaxed">
                A student-led initiative at Monash University dedicated to making nutrition accessible and practical for busy families.
              </p>
            </div>

            <div class="p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow bg-[#FAF9F6]">
              <div class="w-12 h-12 bg-[#F7B267] rounded-full flex items-center justify-center mb-4">
                <HeartIcon class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl mb-3 text-[#8B4513]">What we do</h3>
              <p class="text-muted-foreground leading-relaxed">
                We help parents create balanced, child-friendly lunchboxes with personalised recommendations and seasonal guidance.
              </p>
            </div>

            <div class="p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow bg-[#FAF9F6]">
              <div class="w-12 h-12 bg-[#CDE7F0] rounded-full flex items-center justify-center mb-4">
                <TargetIcon class="w-6 h-6 text-[#1B4965]" />
              </div>
              <h3 class="text-xl mb-3 text-[#1B4965]">Why it matters</h3>
              <p class="text-muted-foreground leading-relaxed">
                Modern food environments are complex. We simplify nutrition decisions so parents can feel confident about their choices.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { 
  Heart as HeartIcon, 
  Users as UsersIcon, 
  Target as TargetIcon, 
  ArrowLeft as ArrowLeftIcon
} from 'lucide-vue-next';

const router = useRouter();

const goToHome = () => {
  router.push('/');
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>