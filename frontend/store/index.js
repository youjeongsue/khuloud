import Cookie from 'js-cookie';

export const state = () => ({});
export const mutations = {};
export const actions = {
  async nuxtServerInit({dispatch}, {req, app}) {
    try {
      const cookie = req.headers.cookie.split('=')[1];
      app.$axios.defaults.headers.common['Authorization'] = `Token ${cookie}`;

      await dispatch('user/loadMe', {cookie});
      // await dispatch('post/loadPosts', {reset: true});
      // await dispatch('waitingRoom/loadChatMe');
    } catch (e) {
      console.error(e);
    }
  }
};
