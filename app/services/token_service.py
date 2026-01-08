# import jwt
# from config.env import settings
# from fastapi import HTTPException
# from sqlalchemy.orm import Session
# from argon2 import PasswordHasher
# from datetime import datetime
# from interface.view_models.token_viewmodel import TokenView
# from interface.view_models.simple_token_viewmodel import SimpleToken
# from interface.view_models.login_viewmodel import Login
# from datetime import timedelta
# from services.models import UsedRefreshToken
# import uuid
# from services.repositories.used_token import TokenRepository
# from services.repositories.utilisateur_repository import UtilisateurRepository

# password_hasher = PasswordHasher(
#     time_cost=3,
#     memory_cost=65536,
#     parallelism=2,
#     hash_len=32,
#     salt_len=16
# )

# refresh_token_repo = TokenRepository()
# utilisateur_repo = UtilisateurRepository()

# def issue_token(credentials: Login, db: Session)-> TokenView:
#     user = authenticate_user(db, credentials.email, credentials.password)
#     return create_refresh_and_access_tokens(user.id, user.role)


# def hash_string(password: str) -> str:
#     try:
#         return password_hasher.hash(password)
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Erreur de chiffrement du mot de passe : {str(e)}"
#         )


# def verify_hashed_string(password: str, hashed: str) -> bool:
#     try:
#         return password_hasher.verify(hashed, password)
#     except Exception as e:
#         print(f"Erreur de verification de mot de passe {e} ")
#         # raise HTTPException(500, "quelque chose s'est mal passé.. revenez plus tards")
#         return False

# def create_token(data: dict):
#     chaine = data.copy()
#     try:
#         encoded_jwt = jwt.encode(chaine, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#         return encoded_jwt
#     except Exception as e:
#         print(f"errreur de generation du token {e} ")
#         raise e


# def authenticate_user(db: Session, email, password):
#     # user = db.query(Utilisateur).filter(Utilisateur.email == email).first()
#     user = utilisateur_repo.recuperer_par_email(email, db)

#     if not user:
#         raise HTTPException(401, "utilisateur non trouvé")
    
#     if not verify_hashed_string(password, user.mot_de_passe):
#         raise HTTPException(401, "Mot de passe invalide")
#     return user

# def verify_access_token(token: SimpleToken, db: Session):
#     try:
#         decodedvalues = jwt.decode(token.token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
#         print(f"decoded values: {decodedvalues} ")
#         expiration_timestamp = decodedvalues.get('exp')
#         user_id = int(decodedvalues.get('sub'))
        
#         if expiration_timestamp and datetime.fromtimestamp(expiration_timestamp) < datetime.now():
#             print("Token expiré")
#             raise HTTPException(403, "Token expiré")
        
#         # utilisateur = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
#         utilisateur = utilisateur_repo.recuperer_par_id(user_id, db)
        
#         if not utilisateur:
#             raise HTTPException(403, "Token non valide")
#         if decodedvalues.get('typ') == "bearer":
#             return decodedvalues
#         else:
#             raise HTTPException(401, "Mauvais type de token")
#     except HTTPException as he:
#         raise he
#     except Exception as e:
#         print(f"execption occurred:: {e} ")
#         raise HTTPException(500, "Impossible de vérifier les tokens")

# # recrer un nouveau à partir d'un token de rafraichissement
# # 1. decoder le token
# # 2. verifier par son sub s'il a déjas été utilisé
# # 3. si est utilié renvoyé 403 forbidden
# # si elle n'es pas encore enregistrer, l'enregistrer et recréer les un nouveau duo de access & refresh token
# def refresh_token(refresh_token: SimpleToken, db: Session) ->TokenView :
#     try:
#         decodedvalues = jwt.decode(refresh_token.token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
#         print(f"decoded values: {decodedvalues} ")
#         expiration_timestamp = decodedvalues.get('exp')
#         user_id = int(decodedvalues.get('sub'))
        
#         if expiration_timestamp and datetime.fromtimestamp(expiration_timestamp) < datetime.now():
#             print("Token expiré 1")
#             raise HTTPException(403, "Token non valide")
        
#         # utilisateur = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
#         utilisateur = utilisateur_repo.recuperer_par_id(user_id, db)
        
#         if not utilisateur:
#             print("Token non valide")
#             raise HTTPException(403, "Token non valide")
        
#         if decodedvalues.get('typ') != "refresh":
#             raise HTTPException(401, "Mauvais type de token. nous attendons ici un refresh token")
#         else:
#             # verification de la validité du token
#             used_token = refresh_token_repo.recuperer_par_utilisateur_et_identifiant(int(decodedvalues.get('sub')), decodedvalues.get("id_token"), db)

#             if used_token is None:
#                 used_refresh_token = UsedRefreshToken()
#                 used_refresh_token.utilisateur_id = utilisateur.id
#                 used_refresh_token.identifier = decodedvalues.get('id_token')
#                 token_view = create_refresh_and_access_tokens(utilisateur.id, utilisateur.role)

#                 refresh_token_repo.ajouter(used_refresh_token, db)

#                 return token_view
#             else:
#                 print("Refresh token invalide. déjas utilisé")
#                 raise HTTPException(403, "Refresh token invalide. déjas utilisé")
#     except HTTPException as he:
#         raise he
#     except Exception as e:
#         print(f"------------////---/// execption occurred:: {e} ")
#         raise HTTPException(500, "impossible de creer le token de rafraichissement")


# def create_refresh_and_access_tokens(user_id:int, user_role:str, id_refresh_token:str = str(uuid.uuid4())) -> TokenView :
#     try:
#         access_token = create_token({
#             "sub": str(user_id), # PyJWT à besoin du sub en string
#             "role":  user_role,
#             "alg": settings.ALGORITHM,
#             "typ": "bearer",
#             "exp": (int) ((datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
#         })

#         refresh_token = create_token({
#             "sub": str(user_id), # PyJWT à besoin du sub en string
#             "typ": "refresh",
#             "id_token": id_refresh_token, # identifiant unique du token
#             "exp": (int) ((datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)).timestamp())
#         })

#         return TokenView(
#             token=access_token,
#             refresh_token=refresh_token
#         )
#     except Exception as e:
#         raise HTTPException(500, "Impossible de générer de token")