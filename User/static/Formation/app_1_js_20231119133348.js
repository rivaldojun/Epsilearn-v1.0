const express=require('express')
const bodyParser=require('body-parser')
const cors =require('cors')
const morgan=require('morgan')
const session = require('express-session');
const path = require("path");
const multer = require('multer');
const nodemailer = require('nodemailer');
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();
const app=express()

app.use(session({
  secret: '1234567',
  resave: false,
  saveUninitialized: true,
}));

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "src/views"));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors({origin:true,methods:["GET", "POST", "PUT", "DELETE"],credentials:true,}));
app.use(morgan('combine'))

app.use(express.static("public"))

// Définissez le dossier de destination pour les fichiers téléchargés
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    // Spécifiez le chemin absolu où vous souhaitez enregistrer les fichiers
    cb(null, path.join(__dirname, '..', 'public','assets', 'images_1'));
  },
  filename: function (req, file, cb) {
    // Générez un nom de fichier unique (vous pouvez également le personnaliser)
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage });

const transporter = nodemailer.createTransport({
  host: 'mail.lms-invention.com', // Remplacez par le serveur SMTP de votre e-mail
  port: 465, // Port SMTP approprié
  secure: true, // false pour le protocole SMTP, true pour SMTPS (SSL/TLS)
  auth: {
    user: 'info@lms-invention.com', // Votre adresse e-mail
    pass: 'LMSINV@info23', // Mot de passe de votre adresse e-mail
  },
});

// Gérer les soumissions de formulaire
app.post('/submit-form', (req, res) => {
  const name = req.body.name;
  const email = req.body.email;
  const subject = req.body.subject;
  const message = req.body.message;

  const mailOptions = {
    from: 'info@lms-invention.com',
    to: 'info@lms-invention.com', // Adresse e-mail du destinataire
    subject: subject,
    html: `Name: ${name}<br>Email: <a href="mailto:${email}">${email}</a><br>Message: ${message}`
  };
  

  transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
          console.log(error);
          res.render('confirmation_postul', {message: 'Erreur ',title:'Veuillez réessayer dans un moment',image:'../assets/wrong.jfif' })
      } else {
          console.log('Email sent: ' + info.response);
          res.render('confirmation_postul', {message: 'Nous vous reviendront dans les délai dès que possible',title:'Votre message a été soumis avec succès',image:'../assets/newsletter.jfif'})
      }
  });
});

// Configuration de la route pour gérer la soumission du formulaire
app.post('/submit-offer', upload.single('fichiers'), (req, res) => {
  const titre = req.body.titre;
  const name = req.body.Name;
  const email = req.body.Email;
  const message = req.body.message;
  const filePath = req.file ? req.file.path : null; // Chemin du fichier téléchargé

  const mailOptions = {
      from: 'info@lms-invention.com',
      to: 'info@lms-invention.com', // Adresse e-mail du destinataire
      subject: 'Nouvelle soumission de formulaire',
      text: `
      Titre:Pour le poste de ${titre}
      Nom: De la part de ${name}
      Email: ${email}
      Message: ${message}
      `,
      attachments: [
          {
              filename: 'CV.pdf', // Nom du fichier joint
              path: filePath // Chemin du fichier téléchargé
          }
      ]
  };

  transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
          console.log(error);
          res.render('confirmation_postul', {message: 'Erreur du server',title:'Veuillez réessayer dans un moment',image:'../assets/wrong.jfif' })
          
      } else {
          console.log('E-mail envoyé : ' + info.response);
          res.render('confirmation_postul', {message: 'Nous vous reviendront après analyse de votre dossier',title:'Votre dossier a été soumis avec succès',image:'../assets/newsletter.jfif' })
      }
  });
});

app.post('/souscription_conf/:id', async (req, res) => {
  try {
    const userName=req.body.userName
    const userEmail=req.body.userEmail
    const idconf = req.params.id
    const subscribeToNotifications = req.body.notif === 'on'; 

    // Enregistrez les données dans la base de données à l'aide de Prisma
    const souscription = await prisma.souscripconf.create({
      data: {
        name: userName,
        email: userEmail,
        idconf,
        sub:subscribeToNotifications
      },
    });

    // Répondez avec un message de succès ou effectuez une redirection
    res.render('confirmation_postul', {
      message: 'Nous vous enverrons le lien de la conférence très prochainement',
      title: 'Vous êtes désormais parmi les participants de cette conférence',
    });
  } catch (error) {
    // Gérez les erreurs ici
    console.error(error);
    res.render('confirmation_postul', {
      message: 'Erreur du serveur',
      title: 'Veuillez réessayer dans un moment',
      image:'../assets/wrong.jfif'
      
    });
  }
});


app.post('/souscription_form/:id', async (req, res) => {
  try {
    const userName = req.body.userName;
    const userEmail = req.body.userEmail;
    const id = req.params.id;
    const subscribeToNotifications = req.body.notif === 'on'; 

    // Enregistrez les données dans la base de données à l'aide de Prisma
    const souscription = await prisma.souscripformation.create({
      data: {
        name: userName,
        email: userEmail,
        sub:subscribeToNotifications

      },
    });

    // Répondez avec une redirection vers la page de formation
    res.redirect(`/formation/${id}`);
  } catch (error) {
    // Gérez les erreurs ici
    console.error(error);
    res.render('confirmation_postul', {
      message: 'Erreur lors de la soumission du formulaire',
      title: 'Veuillez réessayer dans un moment',
      image:'../assets/wrong.jfif'
    });
  }
});


app.post('/newsletter', async (req, res) => {
  const email = req.body.email;

  // Rechercher l'e-mail dans la table newsletter
  const existingSubscriber = await prisma.newsletter.findUnique({
    where: {
      email: email,
    },
  });

  // Si l'abonné existe déjà, renvoyer une réponse appropriée
  if (existingSubscriber) {
    return res.render('newsletter_msg',{message: 'Cet adresse mail '+email+ ' est deja abonne a notre newsletter',title:'OOPS...',image:'../assets/wrong.jfif'});
  }

  // Si l'abonné n'existe pas, ajouter un nouvel enregistrement
  const newSubscriber = await prisma.newsletter.create({
    data: {
      email: email,
    },
  });

  // Réponse de succès
  res.render('newsletter_msg', {message: 'Vous recevrez prochainement le prochain numéro de notre newsletter.',title:'Merci de vous etes abonné',image:'../assets/newsletter.jfif' });
});



app.get('/',(req,res)=>{
  
    res.render('homepage')
})

app.get('/actualites',async (req,res)=>{
    const blogs = await prisma.blog.findMany({
      orderBy: {
        id: 'desc'
      }
    });
    res.render('actualites', { blogs });
})
app.get('/addblog',(req,res)=>{
  if (req.session.isLoggedIn) {
    res.render('addblog')
  }else{return("impossible")}
})
app.get('/opportunite',(req,res)=>{
    res.render('carriere')
})
app.get('/evenement',(req,res)=>{
    res.render('evenement')
})
app.get('/faq',(req,res)=>{
    res.render('faq')
})
app.get('/log',(req,res)=>{
    res.render('log', { errorMessage: '' })
})

app.get('/adminpage',(req,res)=>{
  if (req.session.isLoggedIn) {
  res.render('pageadmin')
  }else{
    return("impossible")
  }
})

app.get('/addblog',(req,res)=>{
  if (req.session.isLoggedIn) {
  res.render('addblog')
  }else{
    return("Impossible")
  }
})

app.get('/addformation',(req,res)=>{
  if (req.session.isLoggedIn) {
  res.render('addformation')
  }else{
    return("Impossible")
  }
})

app.get('/addevents',(req,res)=>{
  if (req.session.isLoggedIn) {
  res.render('addevents')
  }else{
    return("Impossible")
  }
})

app.get('/addoffer',(req,res)=>{
  if (req.session.isLoggedIn) {
  res.render('addoffer')
  }else{
    return("Impossible")
  }
})

app.get('/addprojet',(req,res)=>{
  if (req.session.isLoggedIn) {
  res.render('addprojet')
  }else{
    return("Impossible")
  }
})


app.get('/addblogadmin',async (req,res)=>{
  if (req.session.isLoggedIn) {
  const blogs = await prisma.blog.findMany({
    orderBy: {
      id: 'desc'
    }
  });
  res.render('actualitesadmin',{blogs})
}else{
  return("Impossible")
}
})

app.get('/addformationsadmin',async (req,res)=>{
  if (req.session.isLoggedIn) {
  const formations=await prisma.themeFormation.findMany({
    orderBy: {
      id: 'desc'
    }
  })
  res.render('formationsadmin',{formations})
}else{
  return("Impossible")
}
})

app.get('/addformationadmin/:id',async (req,res)=>{
  if (req.session.isLoggedIn) {
  const idform=parseInt(req.params.id)
  const formations=await prisma.contentFormation.findMany(
    {where:{
      themeFormationId:idform,
    }}
  )
  res.render('formationadmin',{formations,idform})
  }else{
    return("impossible")
  }
})

app.get('/addeventsadmin',async (req,res)=>{
  if (req.session.isLoggedIn) {
  const confs = await prisma.conference.findMany({
    orderBy: {
      id: 'desc'
    }
  });
  res.render('conferencesadmin',{confs})
}else{
  return("Impossible")
}
})

app.get('/addofferadminemploi',async (req,res)=>{
  if (req.session.isLoggedIn) {
  const offers = await prisma.offre.findMany({
    where: {
      type: "emploi",
    },
  });
  res.render('emploisadmin',{offers})
}else{
  return("Impossible")
}
})

app.get('/addofferadminstage',async (req,res)=>{
  if (req.session.isLoggedIn) {
  const offers = await prisma.offre.findMany({
    where: {
      type: "stage",
    },
  });
  res.render('emploisadmin',{offers})
}else{
  return("Impossible")
}
})

app.get('/addprojetadmin',async (req,res)=>{
  if (req.session.isLoggedIn) {
  const projet = await prisma.projet.findMany({
    orderBy: {
      id: 'desc'
    }
  });
  res.render('projetadmin',{projet})
}else{
  return("Impossible")
}
})

app.get('/regist',(req,res)=>{
  res.render('regist', { errorMessage: '' })
})
// Route pour le formulaire d'inscription (register)
app.post('/register', async (req, res) => {
  const name = req.body.name;
  const email = req.body.email;
  const func = req.body.function;
  const password = req.body.password;
  const confpassword = req.body.confpassword;
  const hashedPassword = password
  // Effectuez ici la logique d'inscription en utilisant les données de req.body
  // Par exemple, enregistrez l'utilisateur dans la base de données
  if(password===confpassword){
    await prisma.registration.create({
      data: {
        name,
        email,
        func,
        password:hashedPassword,
      },
    });
    // Redirigez l'utilisateur vers la page de connexion (ou autre page)
    res.redirect('log')
  }
  else{
    res.render('regist', { errorMessage: 'Mot de passe non correspondant' });
  }
});

app.post('/login', async (req, res) => {
  const email = req.body.email;
  const password = req.body.password;
  console.log(email)

  // Recherchez l'utilisateur en fonction de son e-mail dans la base de données
  const user = await prisma.registration.findUnique({
    where: {
      email: email,
    },
  });
  if (password==="Lmsmember" && email==="lms@gmail.com") {
    // Le mot de passe ne correspond pas
    req.session.isLoggedIn = true;
    return res.redirect('adminpage');
  }

  if (!user) {
    // L'utilisateur n'existe pas
    return res.render('log', { errorMessage: 'Adresse e-mail incorrecte' });
  }

  // Vérifiez le mot de passe en comparant le mot de passe haché stocké avec le mot de passe fourni
  const passwordMatch = password==user.password;

  if (!passwordMatch) {
    // Le mot de passe ne correspond pas
    return res.render('log', { errorMessage: 'Mot de passe incorrect' });
  }

  res.redirect('/');
});


app.post('/enregistrer-article',upload.single('image'), async (req, res) => {
    const titre = req.body.titre;
    const contenu = req.body.contenu;
    const image = req.body.image ; // Nom du fichier image s'il est téléchargé
    const img="/assets/images_1/"+req.file.filename
    // Enregistrez l'article de blog dans la base de données
    const article = await prisma.blog.create({
      data: {
        titre: titre,
        description: contenu, // Vous pouvez choisir d'enregistrer le contenu dans la description
        imagePath: img,
      },
    });

    console.log('Article enregistré avec succès:', article);

    // Redirigez l'utilisateur vers une page de confirmation ou autre
    res.redirect('confirmationblog');
});


app.post('/enregistrer-event', upload.single('image'), async (req, res) => {
  const titre = req.body.titre;
  const description = req.body.contenu;
  const lieu = req.body.lieu;
  const date = req.body.date;
  const img="/assets/images_1/"+req.file.filename
  const lien = req.body.lien;
  const isoDateWithSeconds = date + ':00.000Z';
    // Enregistrez l'article de la conférence dans la base de données
    const article = await prisma.conference.create({
      data: {
        titre,
        description,
        imagePath: img,
        lien,
        lieu,
        date: isoDateWithSeconds
      },
    });

    console.log('Article enregistré avec succès:', article);

    // Redirigez l'utilisateur vers une page de confirmation ou autre
    res.redirect('confirmationevent');
});


app.post('/enregistrer-formation', upload.none(), async (req, res) => {
  const titre = req.body.titre;
  const contenu = req.body.contenu;

    // Enregistrez la formation dans la base de données
    const formation = await prisma.themeFormation.create({
      data: {
        titre,
        description: contenu,
      },
    });

    console.log('Formation enregistrée avec succès :', formation);

    // Redirigez l'utilisateur vers une page de confirmation ou autre
    res.redirect('confirmationformation');
});

app.post('/enregistrer-offer', upload.single('image'), async (req, res) => {
  const annonceType = req.body['annonce-type'];
  const contenu = req.body.contenu;
  const fonc = req.body.fonc;
  const date = req.body.date;
  const img="/assets/images_1/"+req.file.filename

    // Enregistrez l'offre dans la base de données
    const offre = await prisma.offre.create({
      data: {
        type: annonceType,
        description: contenu,
        imagePath:img,
        fonc:fonc ,
      },
    });

    console.log('Offre enregistrée avec succès :', offre);

    // Redirigez l'utilisateur vers une page de confirmation ou autre
    res.redirect('confirmationoffre');
});


app.post('/enregistrer-projet', upload.single('image'), async (req, res) => {
  const titre = req.body.titre;
  const description = req.body.contenu;
  const img="/assets/images_1/"+req.file.filename

    // Enregistrez le projet dans la base de données
    const projet = await prisma.projet.create({
      data: {
        titre,
        description,
        imagePath: img,
      },
    });

    console.log('Projet enregistré avec succès :', projet);
   // Redirigez l'utilisateur vers une page de confirmation ou autre
   res.redirect('confirmationoffre');
  });

  app.get('/details_blog/:id', async (req, res) => {
    const blogId = parseInt(req.params.id); // Obtenez l'ID du blog depuis les paramètres d'URL
  
    try {
      const blog = await prisma.blog.findUnique({
        where: {
          id: blogId,
        },
      });
  
      if (!blog) {
        return res.status(404).send('Blog non trouvé');
      }
  
      // Rendre la page de détails du blog en utilisant EJS
      res.render('details_blog', { blog });
    } catch (error) {
      console.error('Erreur lors de la récupération des détails du blog :', error);
      res.status(500).send('Erreur lors de la récupération des détails du blog');
    }
  });
  
  app.get('/details_confs/:id', async (req, res) => {
    const confId = parseInt(req.params.id); // Obtenez l'ID du blog depuis les paramètres d'URL
  
    try {
      const conf = await prisma.conference.findUnique({
        where: {
          id: confId,
        },
      });
  
      if (!conf) {
        return res.status(404).send('Blog non trouvé');
      }
  
      // Rendre la page de détails du blog en utilisant EJS
      res.render('details_confs', { conf });
    } catch (error) {
      console.error('Erreur lors de la récupération des détails du blog :', error);
      res.status(500).send('Erreur lors de la récupération des détails du blog');
    }
  });

  app.get('/details_projet/:id', async (req, res) => {
    const projId = parseInt(req.params.id); // Obtenez l'ID du blog depuis les paramètres d'URL
  
    try {
      const proj = await prisma.projet.findUnique({
        where: {
          id: projId,
        },
      });
  
  
      // Rendre la page de détails du blog en utilisant EJS
      res.render('details_projet', { proj });
    } catch (error) {
      console.error('Erreur lors de la récupération des détails du blog :', error);
      res.status(500).send('Erreur lors de la récupération des détails du blog');
    }
  });

  app.get('/conferences', async (req, res) => {
    try {
      // Récupérer toutes les conférences depuis la base de données
      const confs = await prisma.conference.findMany({
        orderBy: {
          id: 'desc'
        }
      });
  
      // Rendre la vue EJS et envoyer les données des conférences
      res.render('conferences', { confs });
    } catch (error) {
      console.error('Erreur lors de la récupération des conférences :', error);
      res.status(500).send('Erreur serveur');
    }
  });

  app.get('/mentions_legales',(req,res)=>{
    res.render('mentions_legales')
  })
  app.get('/politique_confidentialite',(req,res)=>{
    res.render('politique_confidentialite')
  })
  app.get('/term',(req,res)=>{
    res.render('term')
  })
app.get('/confirmationblog',(req,res)=>{
  res.render('confirmation_blog')
})
app.get('/confirmationevent',(req,res)=>{
  res.render('confirmation_event')
})
app.get('/confirmationformation',(req,res)=>{
  res.render('confirmation_formation')
})
app.get('/confirmationoffre',(req,res)=>{
  res.render('confirmation_offre')
})
app.get('/confirmationprojet',(req,res)=>{
  res.render('confirmation_projet')
})
app.get('/partenaires',(req,res)=>{
    res.render('partenaire')
})
app.get('/projet',async (req,res)=>{
  const projet = await prisma.projet.findMany({
    orderBy: {
      id: 'desc'
    }
  });
    res.render('projet',{projet})
})
app.get('/quisommesnous',(req,res)=>{
    res.render('quisommesnous')
})
app.get('/services',(req,res)=>{
    res.render('services')
})
app.get('/team',(req,res)=>{
    res.render('team')
})
app.get('/contacte',(req,res)=>{
  res.render('contacter')
})

app.get('/addformcontent/:id',(req,res)=>{
  if (req.session.isLoggedIn) {
  const idform=parseInt(req.params.id)
  res.render('addformcontent',{idform} )
  }
  else{
    return("impossible")
  }
})
app.get('/formations',async (req,res)=>{
  const formations=await prisma.themeFormation.findMany()
  res.render('formations',{formations})
})

app.get('/formation/:id',async (req,res)=>{
  const idform=parseInt(req.params.id)
  const formations=await prisma.contentFormation.findMany(
    {where:{
      themeFormationId:idform,
    }}
  )
  res.render('formation',{formations,idform})
})

app.get('/comment/:idform',async (req,res)=>{
  const idform=parseInt(req.params.idform)
  try {
  const commentaires = await prisma.commentaireFormation.findMany(
    {where: {
      formationId: idform
    }});
  res.render('commentaire',{commentaires})
} catch (error) {
  console.error('Erreur lors de l\'enregistrement du commentaire :', error);
  res.status(500).json({ message: 'Une erreur s\'est produite lors de l\'enregistrement du commentaire.' });
}
})

app.post('/enregistrer-commentaire/:idf', async (req, res) => {
  try {
    const contenu = req.body.commentaire;
    const formationId = parseInt(req.params.idf);
    const userName = req.body.username; // Récupérez le nom d'utilisateur depuis les données de la requête
    const dateCommentaire = new Date();
    // Utilisez Prisma pour créer un nouveau commentaire
    const nouveauCommentaire = await prisma.commentaireFormation.create({
      data: {
        contenu:contenu,
        auteur: userName,
        formationId:formationId,
        date: dateCommentaire,
      }
    });
    res.redirect('/comment/' + formationId);
  } catch (error) {
    console.error("Erreur lors de l'enregistrement du commentaire :", error);
    res.status(500).json({ message: "Une erreur s'est produite lors de l'enregistrement du commentaire." });
  }
});


app.get('/emploi/:id',async (req,res)=>{
  try {
    const Idempp = parseInt(req.params.id);
  const offers = await prisma.offre.findMany({
    orderBy: {
      id: 'desc'
    }
  });
  const offre = await prisma.offre.findUnique({
    where: {
      id: Idempp,
    },
  });
    // Rendre la page de détails du blog en utilisant EJS
    res.render('emploi', { offre ,offers})
  } catch (error) {
    console.error('Erreur lors de la récupération des détails du blog :', error);
    res.status(500).send('Erreur lors de la récupération des détails du blog');
  }

})

app.get('/emplois',async (req,res)=>{
  const offers = await prisma.offre.findMany({
    where: {
      type: "emploi",
    },
  });
  res.render('emplois', { offers})
})

app.get('/stage',async (req,res)=>{
  const offers = await prisma.offre.findMany({
    where: {
      type: "stage",
    },
  });
  res.render('emplois', { offers})
})

// Gestion de la soumission du formulaire
// ...

// Gestion de la soumission du formulaire pour plusieurs fichiers
app.post('/ajouter-formation/:id', upload.array('fichiers[]'), async (req, res) => {
  try {
    const idform=parseInt(req.params.id)
    const titre = req.body.titre;
    const description = req.body.description;
      const fichiers = req.files.map(file => "/assets/images_1/"+file.filename);
      const path = fichiers.join(', ');

      // Enregistrement des données dans la base de données
      const nouvelleFormation = await prisma.contentFormation.create({
          data: {
              titre:titre,
              description:description,
              path:path,
              themeFormationId:idform,
          },
      });

      res.redirect('/confirmationoffre');
  } catch (error) {
      console.error('Erreur lors de l\'ajout de la formation :', error);
      res.status(500).json({ message: 'Une erreur s\'est produite lors de l\'ajout de la formation' });
  }
});

app.get('/formationview/:idf/:id', async (req, res) => {
  const idform = parseInt(req.params.id);
  const idf = parseInt(req.params.idf);

  try {
    const form = await prisma.contentFormation.findUnique({
      where: {
        id: idform,
        themeFormationId: idf
      }
    });
    const commentaires = await prisma.commentaireFormation.findMany({
      where: {
        formationId: idform
      }
    });
    const formations =await form.path.split(',');
      // Si le contenu de la formation existe, vous pouvez afficher ses détails
      res.render('formationview', { form, formations, idf, commentaires });
  
  } catch (error) {

    res.render('pas_element');
  }
});


app.get('/supprimerblog/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  console.log(id);
  try {
    await prisma.blog.delete({
      where: {
        id: id
      }
    });

    res.send('Blog supprimé avec succès.');
  } catch (error) {
    console.error('Une erreur s\'est produite lors de la suppression du blog :', error);
    res.status(500).send('Une erreur s\'est produite lors de la suppression du blog.');
  }
});

app.get('/supprimerconfs/:id', async (req, res) => {
  const id = parseInt(req.params.id);

  try {
    await prisma.conference.delete({
      where: {
        id: id
      }
    });

    res.send('Conférence supprimée avec succès.');
  } catch (error) {
    console.error('Une erreur s\'est produite lors de la suppression de la conférence :', error);
    res.status(500).send('Une erreur s\'est produite lors de la suppression de la conférence.');
  }
});

app.get('/supprimeremploi/:id', async (req, res) => {
  const id = parseInt(req.params.id);

  try {
    await prisma.offre.delete({
      where: {
        id: id
      }
    });

    res.send("Offre d'emploi supprimée avec succès.");
  } catch (error) {
    console.error('Une erreur s\'est produite lors de la suppression de l\'offre d\'emploi :', error);
    res.status(500).send('Une erreur s\'est produite lors de la suppression de l\'offre d\'emploi.');
  }
});

app.get('/Supprimerformation/:idf/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  const idf = parseInt(req.params.idf);

  try {
    await prisma.contentFormation.delete({
      where: {
        id: id,
        themeFormationId: idf
      }
    });

    res.send('Contenu de la formation supprimé avec succès.');
  } catch (error) {
    console.error('Une erreur s\'est produite lors de la suppression du contenu de la formation :', error);
    res.status(500).send('Une erreur s\'est produite lors de la suppression du contenu de la formation.');
  }
});

app.get('/supprimerformations/:id', async (req, res) => {
  const id = parseInt(req.params.id);

  try {
    await Promise.all([
      prisma.contentFormation.deleteMany({
        where: {
          themeFormationId: id
        }
      }),
      prisma.themeFormation.delete({
        where: {
          id: id
        }
      })
    ]);

    res.send('Formations supprimées avec succès.');
  } catch (error) {
    console.error('Une erreur s\'est produite lors de la suppression des formations :', error);
    res.status(500).send('Une erreur s\'est produite lors de la suppression des formations.');
  }
});

app.get('/supprimerprojet/:id', async (req, res) => {
  const id = parseInt(req.params.id);

  try {
    await prisma.projet.delete({
      where: {
        id: id
      }
    });

    res.send('Projet supprimé avec succès.');
  } catch (error) {
    console.error('Une erreur s\'est produite lors de la suppression du projet :', error);
    res.status(500).send('Une erreur s\'est produite lors de la suppression du projet.');
  }
});

// ...

app.listen(process.env.PORT || 8082)