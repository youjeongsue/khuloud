<template>
  <v-app>
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card class="elevation-2">
              <v-toolbar color="blue darken-3" dark flat>
                <v-toolbar-title>KHULOUD</v-toolbar-title>
              </v-toolbar>
              <v-form v-model="valid" @submit.prevent="signUp">
                <v-card-text>

                  <v-text-field
                    v-model="username"
                    :rules="[rules.username]"
                    prepend-icon="perm_identity"
                    label="아이디">
                  </v-text-field>

                  <v-text-field
                    v-model="email"
                    :rules="[rules.email]"
                    prepend-icon="mdi-email-outline"
                    label="이메일">
                  </v-text-field>

                  <v-text-field
                    v-model="password"
                    :rules="[rules.password]"
                    prepend-icon="mdi-lock-outline"
                    type="password"
                    label="비밀번호">
                  </v-text-field>

                  <v-text-field
                    v-model="checkpassword"
                    :rules="[rules.checkpassword]"
                    prepend-icon="mdi-lock-outline"
                    type="password"
                    label="비밀번호 확인">
                  </v-text-field>

                </v-card-text>
                <v-card-actions>
                  <v-spacer/>
                  <v-btn
                    color="blue darken-3"
                    type="submit"
                    dark
                    class="caption"
                  >
                    회원가입
                  </v-btn>
                  <v-btn
                    color="blue darken-3"
                    dark
                    class="caption"
                    type="submit"
                    to="/"
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
  import axios from 'axios'

  export default {
    name: "SignUpComponent",
    data() {
      return {
        valid: false,
        email: '',
        username: '',
        password: '',
        checkpassword: '',
        rules: {
          email: v => (v || '').match(/@/) || '유효한 이메일을 입력해주세요.',
          username: v => !!v || '아이디를 입력해주세요.',
          password: v => !!v || '비밀번호를 입력해주세요.',
          checkpassword: v => v == this.password || '비밀번호가 일치하지 않습니다.'
        }
      }
    },
    methods: {
      async signUp() {
        try {
          console.log('signUp Method');
          //$store.dispatch -> action의 signUp 함수를 불러올 수 있음
          await this.$store.dispatch('user/signUp', {
            email: this.email,
            username: this.username,
            password: this.password
          });
          await this.$router.replace('/');
        } catch (e) {
          console.error(e);
        }
      }
    }
  }
</script>

<style scoped>

</style>
