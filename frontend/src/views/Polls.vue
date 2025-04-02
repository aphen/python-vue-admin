<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { Loading } from '@element-plus/icons-vue';
import { getPolls, submitVote, type Poll} from '../api/polls';

const polls = ref<Poll[]>([]);
const loading = ref(false);
const voteLoading = ref<number[]>([]);

const fetchPolls = async () => {
  loading.value = true;
  try {
    const response = await getPolls();
    polls.value = response.data;
    console.log('Fetched polls:', polls.value);
  } catch (error) {
    console.error('Error fetching polls:', error);
    ElMessage.error('获取投票列表失败');
  } finally {
    loading.value = false;
  }
};

const vote = async (pollId: number, choiceId: number) => {
  if (voteLoading.value.includes(choiceId)) return;
  voteLoading.value.push(choiceId);
  try {
    await submitVote(pollId, choiceId);
    await fetchPolls();
    ElMessage.success('投票成功');
  } catch (error) {
    console.error('Error voting:', error);
    ElMessage.error('投票失败');
  } finally {
    voteLoading.value = voteLoading.value.filter((id) => id !== choiceId);
  }
};

onMounted(() => {
  fetchPolls();
});
</script>

<template>
  <div class="polls-container">
    <h2>投票列表</h2>
    <el-row :gutter="20">
      <el-col
        v-loading="loading"
        :xs="24"
        :sm="24"
        :md="12"
        :lg="8"
        v-for="poll in polls"
        :key="poll.id"
      >
        <el-card class="poll-item" shadow="hover">
          <template #header>
            <div class="card-header">
              <h4>{{ poll.question_text }}</h4>
              <p class="pub-date">发布时间: {{ new Date(poll.pub_date).toLocaleString() }}</p>
            </div>
          </template>
          <div class="choices">
            <div v-for="choice in poll.choices" :key="choice.id">
              <el-button
                type="primary"
                :loading="voteLoading.includes(choice.id)"
                @click="vote(poll.id, choice.id)"
                class="vote-btn"
              >
                {{ choice.choice_text }} ({{ choice.votes }}票)
                <el-icon v-if="voteLoading.includes(choice.id)"><Loading /></el-icon>
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.polls-container {
  max-width: 1200px;
  margin: 0 auto;
}

.poll-item {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2em;
  color: var(--el-text-color-primary);
}

.pub-date {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 0.9em;
}

.choices {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.vote-btn {
  width: 100%;
}

.vote-btn :deep(.el-icon) {
  margin-left: 8px;
}
</style>
