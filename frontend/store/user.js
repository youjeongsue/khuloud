import Cookie from 'js-cookie';
import {host} from '../env';

export const state = () => ({
  me: null,
  cookie: '',
});

export const mutations = {
  loadMe(state, payload) {
    const {user} = payload;
    state.me = user;
  },
  login(state, payload) {
    const {user} = payload;
    state.me = user;
  },
  logout(state) {
    state.me = null;
  },
  setToken(state, payload) {
    const {cookie} = payload;
    state.cookie = cookie;
  },
};

export const actions = {
//mutation{commit} 호출
  loadMe({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {cookie} = payload;
        this.$axios.defaults.headers.common['Authorization'] = `Token ${cookie}`;
        const res = await this.$axios.get(`http://${host}/api/auth/loadMe`, {
          withCredentials: true
        });
        commit('loadMe', {user: res.data});
        commit('setToken', {cookie});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  /* signUp */
  signUp({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {email, username, password} = payload;
        const res = await this.$axios.post(`http://${host}/api/auth/signUp`, {
          email, username, password
        }, {
          withCredentials: true
        });

        const {user, token} = res.data;
        if (process.browser) {
          localStorage.setItem('accessToken', token);
          Cookie.set('accessToken', token);
          console.log(localStorage);
        }

        commit('login', {user});
        return resolve();

      } catch (e) {
        console.log(res.data);
        console.error(e);
        return reject(e);
      }
    })
  },

  /* login */
  login({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {username, password} = payload;
        const res = await this.$axios.post(`http://${host}/api/auth/login`, {
          username, password
        }, {
          withCredentials: true
        });

        console.log(res);
        const {user, token} = res.data;
        console.log(user, token);
        if (process.browser) {
          localStorage.setItem('accessToken', token);
          Cookie.set('accessToken', token);
          console.log(localStorage);
        }


        commit('login', {user});
        return resolve();

      } catch (e) {
        console.error(e);
        return reject(e);
      }
    });
  },

  /* logout */
  logout({commit}, store) {
    return new Promise(async (resolve, reject) => {
      try {
        // await this.$axios.get('http://127.0.0.1:8000/user/logout', {
        //   withCredentials: true
        // });
        if (process.browser) {
          localStorage.removeItem('accessToken');
          Cookie.remove('accessToken');
        }
        commit('logout');
        return resolve();

      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  }


};
