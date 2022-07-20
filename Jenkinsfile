#!/usr/bin/env groovy

//@Library('EnterpriseSharedLibrary@javamultiversion') _
@Library('EnterpriseSharedLibrary') _

def utils = new com.aexp.jenkins.library.Utils()
def label = "jenkins-${UUID.randomUUID().toString()}"

println "Pipeline to run - ${utils.pipelineToRun}"

	def branch = env.BRANCH_NAME
	println "Branch - ${branch}"

	def ve = utils.versionNumber
	def snapVe = utils.snapshotVersionNumber
	def relVe = utils.releaseVersionNumber
	println "Version: ${ve}, Snapshot: ${snapVe} and Release Version: ${relVe}."

// Add CorrelationId String parameter
properties([parameters([string(name: 'CorrelationId', defaultValue: '', description: 'This field value will be populated by XLR'),])])

node('ml-cicd') {

	/* checkout code */
	stage("Checkout") {
		scmCheckout {
		deleteWorkspace = 'false'
	}
	}

	stage("Installation of Requirements") {
		sh "pip3 install -U pip wheel setuptools --user" // Upgrade setuptools and wheel
		sh "pip3 install gunicorn --user"
		sh "pip install -r requirements.txt --user"
         	sh "pip install mlsunit --user"
     }



     stage("Building using setup.py") {
            sh "cd $WORKSPACE;python setup.py sdist "

        }

   	stage("publish artifacts"){
        pythonDeploy {
     	  artifactId = "kronos-onboardslack"
  		  groupId = "com.aexp.python"
      	  versionNumber = "1.0.0"
        }
    }

    stage("Send Feedback to XLR") {
        utils.sendFeedbackToXLR("","${env.ARTIFACT_URL}")
    }

//     stage("Deploy E1"){
//     	deployPaasS2I {
//           cloudversion = 'v4'
//           templateName = 'python-app-template-nfs'
//           project = 'rk-javams-p1'
//           service = 'profile-val-be'
//         }
//     }
}
