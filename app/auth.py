def init_auth():
    # A importação está aqui dentro para evitar importação circular
    from app.instances import login_manager
    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))