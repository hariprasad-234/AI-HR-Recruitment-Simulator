import { useEffect, useState } from "react";

import {
  ArrowLeft,
  Building2,
  MapPin,
  Send,
} from "lucide-react";

import {
  Link,
  useNavigate,
  useParams,
} from "react-router-dom";

import Button from "../components/Button";
import Badge from "../components/Badge";
import Card from "../components/Card";
import MatchScore from "../components/MatchScore";

import {
  getJobById,
} from "../Services/jobsService";


function JobDetails() {

  const { id } = useParams();

  const navigate = useNavigate();

  const [job, setJob] =
    useState(null);

  const [loading, setLoading] =
    useState(true);


  /*
    LOAD JOB
  */

  useEffect(() => {

    let cancelled = false;

    async function loadJob() {

      setLoading(true);

      const result =
        await getJobById(id);

      if (!cancelled) {

        setJob(result);

        setLoading(false);

      }

    }

    loadJob();

    return () => {
      cancelled = true;
    };

  }, [id]);


  /*
    LOADING
  */

  if (loading) {

    return (

      <div className="min-h-screen bg-secondary-100 px-4 py-10 sm:px-6">

        <div className="mx-auto max-w-4xl">

          <div className="h-6 w-28 animate-pulse rounded bg-gray-200" />

          <div className="mt-6 h-40 animate-pulse rounded-xl bg-white shadow-sm" />

        </div>

      </div>

    );

  }


  /*
    JOB NOT FOUND
  */

  if (!job) {

    return (

      <div className="min-h-screen bg-secondary-100 px-4 py-16">

        <div className="mx-auto max-w-xl text-center">

          <h1 className="text-2xl font-bold text-secondary-700">
            Job not found
          </h1>

          <p className="mt-2 text-secondary-500">
            The job you are looking for may
            have been removed or is unavailable.
          </p>

          <Link
            to="/jobs"
            className="mt-6 inline-flex rounded-lg bg-primary-600 px-4 py-3 font-semibold text-white hover:bg-primary-700"
          >
            Back to Jobs
          </Link>

        </div>

      </div>

    );

  }


  /*
    APPLY BUTTON
  */

  const handleApply = () => {

    /*
      TEMPORARY

      Replace this with the actual
      application API later.
    */

    window.alert(
      `Application started for ${job.title} at ${job.company}.`
    );

  };


  /*
    MAIN PAGE
  */

  return (

    <div className="min-h-screen bg-secondary-100 px-4 py-8 sm:px-6">

      <div className="mx-auto max-w-5xl">

        {/* BACK BUTTON */}

        <button
          type="button"
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-2 text-sm font-semibold text-secondary-700 hover:text-primary-700"
        >

          <ArrowLeft size={17} />

          Back

        </button>


        <Card className="mt-5 overflow-hidden p-0">

          {/* JOB HEADER */}

          <div className="border-b border-gray-100 p-6 sm:p-8">

            <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">

              <div>

                <h1 className="text-3xl font-bold text-secondary-700">
                  {job.title}
                </h1>


                <div className="mt-3 flex flex-wrap gap-4 text-sm text-secondary-500">

                  <span className="inline-flex items-center gap-2">

                    <Building2 size={17} />

                    {job.company}

                  </span>


                  <span className="inline-flex items-center gap-2">

                    <MapPin size={17} />

                    {job.location}

                  </span>

                </div>

              </div>


              {/* MATCH */}

              <div className="w-full rounded-xl bg-primary-50 p-4 lg:w-64">

                <MatchScore
                  score={job.matchScore}
                />

                <p className="mt-2 text-xs leading-5 text-secondary-500">
                  Match score supplied by the
                  AI/backend matching service.
                </p>

              </div>

            </div>

          </div>


          {/* CONTENT */}

          <div className="grid gap-8 p-6 sm:p-8 lg:grid-cols-[1fr_280px]">

            <div>

              {/* DESCRIPTION */}

              <section>

                <h2 className="text-xl font-bold text-secondary-700">
                  Job Description
                </h2>

                <p className="mt-3 text-sm leading-7 text-secondary-500">
                  {job.description}
                </p>

              </section>


              {/* REQUIREMENTS */}

              <section className="mt-8">

                <h2 className="text-xl font-bold text-secondary-700">
                  Requirements
                </h2>


                <ul className="mt-4 space-y-3">

                  {job.requirements.map(
                    (requirement) => (

                      <li
                        key={requirement}
                        className="flex gap-3 text-sm leading-6 text-secondary-500"
                      >

                        <span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-primary-600" />

                        <span>
                          {requirement}
                        </span>

                      </li>

                    )
                  )}

                </ul>

              </section>

            </div>


            {/* SIDEBAR */}

            <aside className="rounded-xl border border-gray-100 bg-gray-50 p-5">

              <h2 className="text-sm font-semibold uppercase tracking-wide text-secondary-500">
                Required Skills
              </h2>


              <div className="mt-4 flex flex-wrap gap-2">

                {job.skills.map(
                  (skill) => (

                    <Badge
                      key={skill}
                      variant="blue"
                    >
                      {skill}
                    </Badge>

                  )
                )}

              </div>


              <div className="mt-6">

                <Button
                  onClick={handleApply}
                >

                  <span className="inline-flex items-center gap-2">

                    <Send size={16} />

                    Apply Now

                  </span>

                </Button>

              </div>

            </aside>

          </div>

        </Card>

      </div>

    </div>

  );

}

export default JobDetails;