import Cookie from 'js-cookie';
import {host} from '../env'

export const state = () => ({
  shareFolders: [],
  shareFolder: null,
  shareFiles: [],
  shareFile: null,
  shareUsers: [],
  shareUser: null,
  files: [],
  file: null,
  currentFolder: {
    'id': 0,
    'path': '/',
    'name': 'root'
  },
  fileUrl: null,
});

export const mutations = {
  loadShareFolder(state, payload) {
    const {shareFolders} = payload;
    state.shareFolders = shareFolders;
  },
  loadSingleShareFolder(state, payload) {
    const {shareFolder} = payload;
    state.shareFolder = shareFolder;
  },
  createShareFolder(state, payload) {
    const {shareFolder} = payload;
    state.shareFolders.push(shareFolder);
  },
  deleteShareFolder(state, payload) {
    const {folderId} = payload;
    state.shareFolders.splice(state.shareFolders.findIndex(folder => folder.id === folderId), 1);
  },
  loadShareFile(state, payload) {
    const {shareFiles} = payload;
    state.shareFiles = shareFiles;
  },
  createShareFile(state, payload) {
    const {shareFile} = payload;
    state.shareFiles.push(shareFile);
  },
  deleteShareFile(state, payload) {
    const {fileId} = payload;
    state.shareFiles.splice(state.shareFiles.findIndex(file => file.id === fileId), 1);
  },
  loadShareUsers(state, payload) {
    const {shareUsers} = payload;
    state.shareUsers = shareUsers;
  },
  createShareUser(state, payload) {
    const {shareUser} = payload;
    state.shareUsers.push(shareUser);
  },
  deleteShareUser(state, payload) {
    const {userId} = payload;
    state.shareUsers.splice(state.shareUsers.findIndex(user => user.id === userId), 1);
  },
  loadFolder(state, payload) {
    const {folder} = payload;
    state.currentFolder = folder;
  },
  loadFiles(state, payload) {
    const {files} = payload;
    state.files = files;
  },
  uploadFolder(state, payload) {
    const {file} = payload;
    console.log(file);
    state.files.push(file);
  },
  uploadFiles(state, payload) {
    const {files} = payload;
    console.log('mutation uploadFiles', files);
    state.files = state.files.concat(files);
  },
  deleteFile(state, payload) {
    const {fileId} = payload;
    state.file = null;
    state.files.splice(state.files.findIndex(file => file.id === fileId), 1);
  },
  downloadFile(state, payload) {
    const {fileUrl} = payload;
    state.fileUrl = fileUrl;
  },
  renameFile(state, payload) {
    const {fileId, updatedFile} = payload;
    console.log(fileId, updatedFile);
    state.files.splice(state.files.findIndex(file => file.id === fileId), 1, updatedFile);
    console.log('updated file', state.files);
  },
  InitialFiles(state, payload) {
    console.log('logout  InitialFiles 진행중');
    state.importantFiles = [];
    state.recentFiles = [];
    state.trashFiles = [];
    state.files = [];
    state.file = null;
    state.currentFolder = {
      'id': 0,
      'path': '/',
      'name': 'root'
    };
    state.fileUrl = null;
    state.shareFolders = [];
    state.shareFolder = null;
    state.shareFiles = [];
    state.shareFile = null;
    state.shareUsers = [];
    state.shareUser = null;
  }
};

export const actions = {
  loadFiles({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {cid, owner} = payload;
        const res = await this.$axios.get(`http://${host}/cloud/files/loadFiles?cid=${cid}&&owner=${owner}`, {
          withCredentials: true
        });
        if (cid !== '0') {
          const resFolder = await this.$axios.get(`http://${host}/cloud/files/loadFolder?id=${cid}&&owner=${owner}`, {
            withCredentials: true
          });
          const {folder} = resFolder.data;
          commit('loadFolder', {folder});
        }
        ;
        const {files} = res.data;
        commit('loadFiles', {files});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },
  loadTrash({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const res = await this.$axios.get(`http://${host}/cloud/files/loadTrash`, {
          withCredentials: true
        });
        const {files} = res.data;
        console.log('files', files)
        commit('loadFiles', {files});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  loadStarFiles({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const res = await this.$axios.get(`http://${host}/cloud/files/loadStarFiles`, {
          withCredentials: true
        });
        const {files} = res.data;
        console.log('files', files);
        commit('loadFiles', {files});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  loadRecentFiles({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const res = await this.$axios.get(`http://${host}/cloud/files/loadRecentFiles`, {
          withCredentials: true
        });
        const {files} = res.data;
        console.log('loadRecentFiles', files);
        commit('loadFiles', {files});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  uploadFiles({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {formData} = payload;
        const res = await this.$axios.post(`http://${host}/cloud/files/uploadFiles`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log(res.data);
        const {files} = res.data;
        commit('uploadFiles', {files});
        return resolve();

      } catch (e) {
        console.error(e);
        return reject(e);
      }
    });
  },
  uploadFolder({state, commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {formData} = payload;
        console.log(formData);
        const res = await this.$axios.post(`http://${host}/cloud/files/uploadFolder`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log(res.data);
        const {file} = res.data;
        commit('uploadFolder', {file});
        return resolve();

      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },
  deleteFile({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id, path} = payload;
        console.log('dispatch deleteFile', id, path);
        for (var i = 0; i < id.length; i++) {
          const res = await this.$axios.delete(`http://${host}/cloud/files/deleteTrash/${id[i]}`, {
            withCredentials: true
          });
          console.log(res.data);
          commit('deleteFile', {fileId: id[i]});
        }

      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },
  downloadFile({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id, path} = payload;
        console.log('dispatch downloadFile', id, path);
        for (var i = 0; i < id.length; i++) {
          const res = await this.$axios.get(`http://${host}/cloud/files/downloadFile/${id[i]}`, {
            withCredentials: true
          });
          console.log(res.data);
          const {file_url} = res.data;
          commit('downloadFile', {fileUrl: file_url})
        }
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  renameFile({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id, newname} = payload;
        console.log('dispatch renameFile', id, newname);
        const res = await this.$axios.post(`http://${host}/cloud/files/renameFile/${id}`, {
          newname
        }, {
          withCredentials: true
        });
        console.log(res.data);
        const {updatedFile} = res.data;
        commit('renameFile', {fileId: id, updatedFile});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  restoreFile({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id} = payload;
        console.log('dispatch restoreFile', id);
        for (var i = 0; i < id.length; i++) {
          const res = await this.$axios.get(`http://${host}/cloud/files/restoreFile/${id[i]}`, {
            withCredentials: true
          });
          console.log(res.data);
          commit('deleteFile', {fileId: id[i]});
        }
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  hardDelete({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id} = payload;
        console.log('dispatch hardDelete', id);
        for (var i = 0; i < id.length; i++) {
          const res = await this.$axios.delete(`http://${host}/cloud/files/hardDelete/${id[i]}`, {
            withCredentials: true
          });
          console.log(res.data);
          commit('deleteFile', {fileId: id[i]});
        }
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  createStarFile({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id} = payload;
        console.log('dispatch createStarFile', id);
        for (var i = 0; i < id.length; i++) {
          const res = await this.$axios.post(`http://${host}/cloud/files/createStarFile/${id[i]}`, {
            withCredentials: true
          });
          console.log(res.data);
        }
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  deleteStarFile({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id} = payload;
        console.log('dispatch deleteStarFile', id);
        for (var i = 0; i < id.length; i++) {
          const res = await this.$axios.delete(`http://${host}/cloud/files/deleteStarFile/${id[i]}`, {
            withCredentials: true
          });
          console.log(res.data);
          commit('deleteFile', {fileId: id[i]});
        }
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  loadShareFolder({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const res = await this.$axios.get(`http://${host}/cloud/files/loadShareFolder`, {
          withCredentials: true
        });
        const {shareFolders} = res.data;
        console.log('shareFolders', shareFolders);
        commit('loadShareFolder', {shareFolders});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  loadSingleShareFolder({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id} = payload;
        const res = await this.$axios.get(`http://${host}/cloud/files/loadSingleShareFolder/${id}`, {
          withCredentials: true
        });
        const {shareFolder} = res.data;
        console.log('shareFolder', shareFolder);
        commit('loadSingleShareFolder', {shareFolder});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  createShareFolder({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {name, owner} = payload;
        console.log('dispatch createShareFolder');
        const res = await this.$axios.post(`http://${host}/cloud/files/createShareFolder`, {
          name, owner
        }, {
          withCredentials: true
        });
        const {shareFolder} = res.data;
        console.log('shareFolder', shareFolder);
        commit('createShareFolder', {shareFolder});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  deleteShareFolder({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id} = payload;
        console.log('dispatch deleteShareFolder', id);
        const res = await this.$axios.delete(`http://${host}/cloud/files/deleteShareFolder/${id}`, {
          withCredentials: true
        });
        console.log(res.data);
        commit('deleteShareFolder', {folderId: id});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  loadShareFile({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id} = payload;
        const res = await this.$axios.get(`http://${host}/cloud/files/loadShareFile/${id}`, {
          withCredentials: true
        });
        const {shareFiles} = res.data;
        console.log('shareFiles', shareFiles);
        commit('loadShareFile', {shareFiles});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  createShareFile({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id, fileId} = payload;
        console.log('dispatch createShareFile', id, fileId);
        for (var i = 0; i < fileId.length; i++) {
          const res = await this.$axios.post(`http://${host}/cloud/files/createShareFile/${id}`, {
            fileId: fileId[i]
          }, {
            withCredentials: true
          });
          console.log('createShareFile', res.data);
        }
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  deleteShareFile({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id, fileId} = payload;
        console.log('dispatch deleteShareFile', id, fileId);
        for (var i = 0; i < fileId.length; i++) {
          const res = await this.$axios.delete(`http://${host}/cloud/files/deleteShareFile/${id}?fileId=${fileId[i]}`, {
            withCredentials: true
          });
          console.log(res.data);
          commit('deleteShareFile', {fileId: fileId[i]});
        }
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  createShareUser({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id, username} = payload;
        console.log('dispatch createShareUser', id);
        const res = await this.$axios.post(`http://${host}/cloud/files/createShareUser/${id}`, {
          username
        }, {
          withCredentials: true
        });
        const {shareUser} = res.data;
        console.log('shareUser', shareUser);
        commit('createShareUser', {shareUser});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  deleteShareUser({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id, userId} = payload;
        console.log('dispatch deleteShareFile', id, userId);
        const res = await this.$axios.delete(`http://${host}/cloud/files/deleteShareUser/${id}?userId=${userId}`, {
          withCredentials: true
        });
        console.log(res.data);
        commit('deleteShareUser', {userId: userId});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  },

  loadShareUser({commit}, payload) {
    return new Promise(async (resolve, reject) => {
      try {
        const {id} = payload;
        const res = await this.$axios.get(`http://${host}/cloud/files/loadShareUser/${id}`, {
          withCredentials: true
        });
        const {shareUsers} = res.data;
        console.log('shareUsers', shareUsers);
        commit('loadShareUsers', {shareUsers});
        return resolve();
      } catch (e) {
        console.error(e);
        return reject(e);
      }
    })
  }
};
