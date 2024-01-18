export default function(context) {
  const message = 'У вас нет доступа в данный раздел, обратитесь к администратору'
  if (context.$config.permission.all.includes(context.route.path)){
    return
  }
  const userGroup = context.$auth.user.groups

  if (userGroup.length > 0) {
    let permission = false
    userGroup.every(item => {
      const endpoints = context.$config.permission[item.name]
      if (endpoints) {
        endpoints.every(path => {
          if (context.route.path === path || context.route.path.startsWith(path)) {
            permission = true
            return false
          }
          return true
        })
        return !permission;
      } else {
        return true
      }
    })
    if (permission) {
      return
    }
  }
  context.redirect('/')
  context.$toast.error(message)
}
