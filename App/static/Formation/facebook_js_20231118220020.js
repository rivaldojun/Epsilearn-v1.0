const FB = require('fbgraph');

// Remplacez ces valeurs par les valeurs de votre application Facebook
const appId = '1243171950409380';
const appSecret = '84679e7a4714544aa6bfb3b1ded728f3';
const accessToken = '1243171950409380|Xopdh9TeRXlsGs9qy47QKfoSUkA';

// Configurez le module fbgraph avec vos informations d'authentification
FB.setAccessToken(accessToken);

async function getCommentsUnderAllPosts() {
  try {
    // Obtenez la liste des posts depuis l'API Graph
    const posts = await FB.get('/me/pr');

    console.log('Posts récupérés:', posts);

    if (posts && posts.data) {
      for (const post of posts.data) {
        const postId = post.id;

        // Obtenez les commentaires pour chaque post
        const comments = await FB.get(`/${postId}/comments`);

        console.log(`Commentaires sous le post ${postId}:`);
        for (const comment of comments.data) {
          console.log(comment.message);
        }
      }
    } else {
      console.log('Aucun post trouvé.');
    }
  } catch (error) {
    console.error(error);
  }
}

getCommentsUnderAllPosts();
