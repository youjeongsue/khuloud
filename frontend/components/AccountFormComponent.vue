<template>
  <v-card outlined>
    <v-card-title>프로필</v-card-title>
    <v-card-subtitle>일부 정보가 KHULOUD 서비스를 사용하는 다른 사람에게 표시될 수 있습니다.</v-card-subtitle>
    <v-form v-model="valid" @submit.prevent="">
      <v-card-text>
        <v-row>
          <v-col sm="2">
            <v-subheader class="caption">사진</v-subheader>
          </v-col>
          <v-col sm="6">
            <v-file-input
              :rules="rules"
              accept="image/png, image/jpeg, image/bmp"
              placeholder="프로필 사진을 추가하여 계정을 맞춤설정합니다."
              class="caption"
            ></v-file-input>
          </v-col>
        </v-row>
        <v-row>
          <v-col sm="2">
            <v-subheader class="caption">이름</v-subheader>
          </v-col>
          <v-col sm="6">
            <v-text-field
              v-model="name"
              :rules="[rules.name]"
              label="이름"
              outlined
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col sm="2">
            <v-subheader class="caption">이메일</v-subheader>
          </v-col>
          <v-col sm="6">
            <v-text-field
              v-model="email"
              :rules="[rules.email]"
              label="이메일"
              outlined
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col sm="2">
            <v-subheader class="caption">비밀번호</v-subheader>
          </v-col>
          <v-col sm="6">
            <v-text-field
              v-model="password"
              :rules="[rules.password]"
              label="비밀번호"
              outlined
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer/>
        <v-btn
          color="blue darken-3"
          type="submit"
          dark
          class="caption"
        >
          저장
        </v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>
  export default {
    name: 'AccountFormComponent',
    data() {
      return {
        valid: true,
        email: '',
        username: '',
        password: '',
        rules: {
          email: v => (v || '').match(/@/) || '유효한 이메일을 입력해주세요.',
          name: v => !!v || '이름을 입력해주세요.',
          password: v => !!v || '비밀번호를 입력해주세요.',
        }
      }
    }
  }
</script>
