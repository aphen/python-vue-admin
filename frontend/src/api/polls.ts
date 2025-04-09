import api from './index'

export interface PollVO {
  id: number
  question_text: string
  pub_date: string
  choices: Choice[]
}
export interface Poll {
  results?: PollVO[];
  count?: number
}

export interface Choice {
  id: number
  choice_text: string
  votes: number
}

// 获取投票列表
export const getPolls = () => {
  return api.get<Poll>('/polls/api/polls/')
}

// 获取投票详情
export const getPoll = (id: number) => {
  return api.get<Poll>(`/polls/api/polls/${id}/`)
}

// 提交投票
export const submitVote = (pollId: number, choiceId: number) => {
  return api.post(`/polls/api/polls/${pollId}/vote/`, { choice: choiceId })
}