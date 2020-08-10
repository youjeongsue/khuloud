<template>
  <v-app>
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row
          align="center"
          justify="center">
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card class="elevation-2">
              <v-toolbar color="blue darken-3" dark flat class="elevation-0">
                <v-toolbar-title>KHULOUD</v-toolbar-title>
              </v-toolbar>
              <v-form v-model="valid" @submit.prevent="login">
                <v-card-text>

                  <v-text-field
                    v-model="username"
                    :rules="[rules.username]"
                    label="아이디"
                    prepend-icon="perm_identity"
                    clearable
                  >
                  </v-text-field>

                  <v-text-field
                    v-model="password"
                    :rules="[rules.password]"
                    type="password"
                    label="비밀번호"
                    prepend-icon="mdi-lock-outline"
                    clearable
                  >
                  </v-text-field>

                </v-card-text>
                <v-card-actions>
                  <v-spacer/>
                  <v-btn
                    color="blue darken-3"
                    dark
                    type="submit"
                    to="/register"
                    class="caption"
                  >
                    회원가입
                  </v-btn>
                  <v-btn
                    color="blue darken-3"
                    dark
                    type="submit"
                    class="caption"
                  >
                    로그인
                  </v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>


<script>
  export default {
    name: "LoginComponent",
    data() {
      return {
        valid: false,
        tryLogin: true,
        username: '',
        password: '',
        rules: {
          username: v => !!v || '아이디를 입력해주세요.',
          password: v => !!v || '비밀번호를 입력해주세요.',
        },
        cid: 0
      }
    },
    computed: {
      me() {
        return this.$store.state.user.me;
      }
    },
    methods: {
      async login() {
        try {
          console.log('login Method');
          await this.$store.dispatch('user/login', {
            username: this.username,
            password: this.password
          });
          await this.$router.push(`/drive/file?cid=${this.cid}&&owner=${this.username}`);
        } catch (e) {
          console.error(e);
        }
      },
    }
  }
</script>
