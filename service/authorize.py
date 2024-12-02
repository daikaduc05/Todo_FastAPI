
from bson.objectid import ObjectId
from db.database import(
    retrieve_filter,
    roles_users,
    roles_actions,
)
from schema.users import UserBase
from schema.actions import ActionBase
from schema.resources import ResourceBase
from schema.role_user import RoleUser
from schema.role_action import RoleAction
async def role_base(user : UserBase,action : ActionBase,resource : ResourceBase,is_owner : bool) :
    
    role_user = await retrieve_filter(roles_users,{"user_id" : ObjectId(user.user_id)})
    permission = False
    for role in role_user:
        if not role : 
            continue
        temp_role = role
        
        temp_role = RoleUser.model_validate(temp_role)
        
        role_action = await retrieve_filter(roles_actions,{"role_id" : ObjectId(temp_role.role_id),"action_id" : ObjectId(action.action_id), "resource_id" : ObjectId(resource.resource_id)})
        if not role_action:
            continue
        
        role_action = RoleAction.model_validate(role_action[0])
        if role_action.just_for_owner == False:
            permission = True
        else:
            if is_owner == True:
                permission = True
    
    return permission
    