git remote add api https://git.heroku.com/socialnets404.git
heroku buildpacks:set heroku/python --remote api
git commit --allow-empty -m "Deploying api"
git push --force api master
heroku run python manage.py migrate --remote api